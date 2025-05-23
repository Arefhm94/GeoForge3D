import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { spawn } from "child_process";
import path from "path";
import fs from "fs";
import { geoDataSchema } from "../shared/schema";
import { db } from "@db";
import { geoData, analysisResults } from "@shared/schema";
import { eq } from "drizzle-orm";

export async function registerRoutes(app: Express): Promise<Server> {
  // API prefix
  const apiPrefix = "/api";
  
  // Get all geo data
  app.get(`${apiPrefix}/geodata`, async (req, res) => {
    try {
      const allGeoData = await db.query.geoData.findMany({
        orderBy: (geoData, { desc }) => [desc(geoData.createdAt)],
      });
      
      return res.json(allGeoData);
    } catch (error) {
      console.error("Error fetching geo data:", error);
      return res.status(500).json({ error: "Failed to fetch geo data" });
    }
  });
  
  // Create new geo data
  app.post(`${apiPrefix}/geodata`, async (req, res) => {
    try {
      const { name, description, geojson, area } = req.body;
      
      // For simplicity, we're not requiring authentication now
      // In a real app, you would get the userId from the authenticated user
      const userId = null;
      
      const [result] = await db.insert(geoData).values({
        userId,
        name,
        description,
        geojson,
        area,
      }).returning();
      
      return res.status(201).json(result);
    } catch (error) {
      console.error("Error creating geo data:", error);
      return res.status(500).json({ error: "Failed to create geo data" });
    }
  });
  
  // Run analysis
  app.post(`${apiPrefix}/analyze/:moduleType`, async (req, res) => {
    try {
      const { moduleType } = req.params;
      const { geojson, options } = req.body;
      
      if (!geojson) {
        return res.status(400).json({ error: "GeoJSON data is required" });
      }
      
      // Execute Python script based on module type
      const scriptPath = path.join(__dirname, `python/${moduleType.replace(/-/g, '_')}.py`);
      
      // Check if the script exists
      if (!fs.existsSync(scriptPath)) {
        return res.status(404).json({ error: `Analysis module '${moduleType}' not found` });
      }
      
      // Create temporary file for GeoJSON input
      const tempInputFile = path.join(__dirname, `temp_${Date.now()}.json`);
      fs.writeFileSync(tempInputFile, JSON.stringify(geojson));
      
      // Execute Python script
      const pythonProcess = spawn('python', [
        scriptPath,
        tempInputFile,
        JSON.stringify(options || {})
      ]);
      
      let scriptOutput = '';
      let scriptError = '';
      
      pythonProcess.stdout.on('data', (data) => {
        scriptOutput += data.toString();
      });
      
      pythonProcess.stderr.on('data', (data) => {
        scriptError += data.toString();
      });
      
      pythonProcess.on('close', async (code) => {
        // Clean up temp file
        try {
          fs.unlinkSync(tempInputFile);
        } catch (error) {
          console.error("Error cleaning up temp file:", error);
        }
        
        if (code !== 0) {
          console.error(`Python process exited with code ${code}`);
          console.error(scriptError);
          return res.status(500).json({ 
            error: "Analysis failed", 
            details: scriptError
          });
        }
        
        try {
          const analysisOutput = JSON.parse(scriptOutput);
          
          // Store result in database if there's a geoDataId
          if (req.body.geoDataId) {
            await db.insert(analysisResults).values({
              geoDataId: req.body.geoDataId,
              moduleType,
              results: analysisOutput
            });
          }
          
          return res.json(analysisOutput);
        } catch (error) {
          console.error("Error parsing analysis results:", error);
          console.error("Raw output:", scriptOutput);
          return res.status(500).json({ 
            error: "Failed to parse analysis results",
            details: error
          });
        }
      });
    } catch (error) {
      console.error("Error during analysis:", error);
      return res.status(500).json({ error: "Analysis failed" });
    }
  });
  
  // Get pricing information
  app.get(`${apiPrefix}/pricing`, (req, res) => {
    return res.json({
      freeArea: 100, // Square meters
      extraChunkSize: 10, // Square meters per chunk
      pricePerChunk: 0.10, // Price in USD per extra chunk
    });
  });
  
  // Get analysis results by geo data ID
  app.get(`${apiPrefix}/geodata/:id/results`, async (req, res) => {
    try {
      const { id } = req.params;
      const results = await db.query.analysisResults.findMany({
        where: eq(analysisResults.geoDataId, parseInt(id)),
        orderBy: (analysisResults, { desc }) => [desc(analysisResults.createdAt)],
      });
      
      return res.json(results);
    } catch (error) {
      console.error("Error fetching analysis results:", error);
      return res.status(500).json({ error: "Failed to fetch analysis results" });
    }
  });
  
  // Building footprints API endpoint
  app.get(`${apiPrefix}/buildings`, async (req, res) => {
    try {
      const { north, south, east, west, sources = 'osm,microsoft' } = req.query;
      
      // Validate parameters
      if (!north || !south || !east || !west) {
        return res.status(400).json({ 
          error: 'Missing required parameters: north, south, east, west'
        });
      }
      
      // Check if values are valid numbers
      const coordinates = { north, south, east, west };
      for (const [key, value] of Object.entries(coordinates)) {
        const num = parseFloat(value as string);
        if (isNaN(num)) {
          return res.status(400).json({ 
            error: `Invalid ${key} coordinate: ${value}`
          });
        }
      }
      
      // Run the Python script to fetch building footprints
      const pythonScript = path.resolve(__dirname, 'python/fetch_buildings.py');
      
      const pythonProcess = spawn('python', [
        pythonScript,
        '--north', north as string,
        '--south', south as string,
        '--east', east as string,
        '--west', west as string,
        '--sources', sources as string,
        '--format', 'geojson'
      ]);
      
      let jsonData = '';
      let errorOutput = '';
      
      pythonProcess.stdout.on('data', (data) => {
        jsonData += data.toString();
      });
      
      pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });
      
      pythonProcess.on('close', (code) => {
        if (code !== 0) {
          console.error(`Python script exited with code ${code}`);
          console.error(errorOutput);
          return res.status(500).json({ 
            error: 'Failed to fetch building footprints',
            details: errorOutput
          });
        }
        
        try {
          // Parse the JSON output from the Python script
          const buildingData = JSON.parse(jsonData);
          res.json(buildingData);
        } catch (err) {
          console.error('Error parsing JSON output:', err);
          res.status(500).json({ 
            error: 'Failed to parse building footprints data',
            details: jsonData
          });
        }
      });
      
    } catch (error) {
      console.error('Error fetching building footprints:', error);
      res.status(500).json({ 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : String(error)
      });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
