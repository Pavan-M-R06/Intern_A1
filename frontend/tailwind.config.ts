import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "rgb(2 6 23)",
        foreground: "rgb(248 250 252)",
        card: "rgb(15 23 42)",
        "card-foreground": "rgb(248 250 252)",
        popover: "rgb(15 23 42)",
        "popover-foreground": "rgb(248 250 252)",
        primary: "rgb(124 58 237)",
        "primary-foreground": "rgb(248 250 252)",
        secondary: "rgb(6 182 212)",
        "secondary-foreground": "rgb(248 250 252)",
        muted: "rgb(51 65 85)",
        "muted-foreground": "rgb(148 163 184)",
        accent: "rgb(124 58 237)",
        "accent-foreground": "rgb(248 250 252)",
        destructive: "rgb(239 68 68)",
        "destructive-foreground": "rgb(248 250 252)",
        border: "rgb(51 65 85)",
        input: "rgb(30 41 59)",
        ring: "rgb(124 58 237)",
      },
      borderRadius: {
        lg: "0.5rem",
        md: "calc(0.5rem - 2px)",
        sm: "calc(0.5rem - 4px)",
      },
    },
  },
  plugins: [],
};

export default config;
