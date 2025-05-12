import { db } from "@db";
import * as schema from "@shared/schema";
import { eq } from "drizzle-orm";

export const storage = {
  // GeoData operations
  async getAllGeoData() {
    return db.query.geoData.findMany({
      orderBy: (geoData, { desc }) => [desc(geoData.createdAt)],
    });
  },
  
  async getGeoDataById(id: number) {
    return db.query.geoData.findFirst({
      where: eq(schema.geoData.id, id),
    });
  },
  
  async createGeoData(data: schema.InsertGeoData) {
    const [result] = await db.insert(schema.geoData)
      .values(data)
      .returning();
    return result;
  },
  
  async deleteGeoData(id: number) {
    return db.delete(schema.geoData)
      .where(eq(schema.geoData.id, id))
      .returning();
  },
  
  // Analysis results operations
  async getAnalysisResultsByGeoDataId(geoDataId: number) {
    return db.query.analysisResults.findMany({
      where: eq(schema.analysisResults.geoDataId, geoDataId),
      orderBy: (analysisResults, { desc }) => [desc(analysisResults.createdAt)],
    });
  },
  
  async createAnalysisResult(data: schema.InsertAnalysisResults) {
    const [result] = await db.insert(schema.analysisResults)
      .values(data)
      .returning();
    return result;
  },
};
