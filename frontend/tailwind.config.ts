import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        kapruka: {
          maroon: "#7A1F2B",
          gold: "#C9A227",
          cream: "#F7F1E8",
          ink: "#1C1412",
        },
      },
    },
  },
  plugins: [],
};

export default config;
