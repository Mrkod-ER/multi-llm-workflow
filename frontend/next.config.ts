import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable standalone output for optimized Docker production builds
  output: "standalone",

  // Proxy /api/* requests to the FastAPI backend during production
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL ?? "http://backend:8000"}/api/v1/:path*`,
      },
    ];
  },
};

export default nextConfig;
