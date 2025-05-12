import { pgTable, text, serial, integer, boolean, jsonb, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";
import { relations } from "drizzle-orm";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;

// Table for storing GeoJSON data
export const geoData = pgTable("geo_data", {
  id: serial("id").primaryKey(),
  userId: integer("user_id").references(() => users.id),
  name: text("name").notNull(),
  description: text("description"),
  geojson: jsonb("geojson").notNull(),
  area: integer("area").notNull(), // Area in square meters
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const geoDataRelations = relations(geoData, ({ one }) => ({
  user: one(users, {
    fields: [geoData.userId],
    references: [users.id],
  }),
}));

export const insertGeoDataSchema = createInsertSchema(geoData).pick({
  userId: true,
  name: true,
  description: true,
  geojson: true,
  area: true,
});

export type InsertGeoData = z.infer<typeof insertGeoDataSchema>;
export type GeoData = typeof geoData.$inferSelect;

// Table for storing analysis results
export const analysisResults = pgTable("analysis_results", {
  id: serial("id").primaryKey(),
  geoDataId: integer("geo_data_id").references(() => geoData.id).notNull(),
  moduleType: text("module_type").notNull(), // e.g., "land-cover", "elevation", etc.
  results: jsonb("results").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const analysisResultsRelations = relations(analysisResults, ({ one }) => ({
  geoData: one(geoData, {
    fields: [analysisResults.geoDataId],
    references: [geoData.id],
  }),
}));

export const insertAnalysisResultsSchema = createInsertSchema(analysisResults).pick({
  geoDataId: true,
  moduleType: true,
  results: true,
});

export type InsertAnalysisResults = z.infer<typeof insertAnalysisResultsSchema>;
export type AnalysisResults = typeof analysisResults.$inferSelect;
