import { db } from "./index";
import * as schema from "@shared/schema";

async function seed() {
  try {
    // Check if we already have seed data
    const existingData = await db.query.geoData.findMany();
    
    if (existingData.length > 0) {
      console.log("Seed data already exists. Skipping seed operation.");
      return;
    }
    
    // Create a sample user
    const [user] = await db.insert(schema.users).values({
      username: "demo",
      password: "demo123", // In a real app, this would be hashed
    }).returning();
    
    // Create sample geo data
    const [geoDataSample] = await db.insert(schema.geoData).values({
      userId: user.id,
      name: "Central Park Area",
      description: "Sample area covering part of Central Park in New York City",
      geojson: {
        type: "Feature",
        properties: {},
        geometry: {
          type: "Polygon",
          coordinates: [[
            [-73.9676, 40.7729],
            [-73.9676, 40.7829],
            [-73.9576, 40.7829],
            [-73.9576, 40.7729],
            [-73.9676, 40.7729]
          ]]
        }
      },
      area: 120000, // Area in square meters
    }).returning();
    
    // Create sample analysis results
    await db.insert(schema.analysisResults).values({
      geoDataId: geoDataSample.id,
      moduleType: "land-cover",
      results: {
        landCover: [
          { label: "Urban/Built-up", percentage: 48, color: "bg-gray-600" },
          { label: "Forest", percentage: 32, color: "bg-green-600" },
          { label: "Water", percentage: 15, color: "bg-blue-600" },
          { label: "Other", percentage: 5, color: "bg-orange-500" }
        ],
        summary: [
          "The selected area is primarily urban (48%) with significant forest cover (32%).",
          "Water bodies make up 15% of the area, providing recreational opportunities.",
          "The mix of urban and natural areas creates a unique urban park ecosystem."
        ]
      }
    });
    
    console.log("Seed data created successfully");
  } 
  catch (error) {
    console.error("Error seeding database:", error);
  }
}

seed();
