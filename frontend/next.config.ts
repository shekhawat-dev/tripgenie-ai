import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  allowedDevOrigins: ["172.20.198.107"],
  typescript: {
    ignoreBuildErrors: true,
  },
};

export default nextConfig;