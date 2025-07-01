import React from "react";
import ReactDOM from "react-dom/client";
import { ChakraProvider, extendTheme } from "@chakra-ui/react";

import App from "./App";

// Define our custom dark theme
const theme = extendTheme({
  styles: {
    global: {
      body: {
        bg: "#0A0A0A", // Very dark background
        color: "#E0E0E0", // Light grey text
        fontFamily: "Roboto Mono, monospace", // Monospace font
      },
    },
  },
  colors: {
    brand: {
      50: "#e0f7fa",
      100: "#b2ebf2",
      200: "#80deea",
      300: "#4dd0e1",
      400: "#26c6da",
      500: "#00bcd4",
      600: "#00acc1",
      700: "#0097a7",
      800: "#00838f",
      900: "#006064",
    },
    terminalGreen: "#00A040", // Soft green for terminal text
    terminalBlue: "#4080C0", // Muted blue for accents
    darkBackground: "#0A0A0A", // Main very dark background
    panelBackground: "#1A1A1A", // Slightly lighter dark for panels
    borderColor: "#444444", // Subtle border color
    lightText: "#E0E0E0", // General light text
    accentBlue: "#88CCFF", // Muted blue for accents/headings
  },
  fonts: {
    body: "Roboto Mono, monospace",
    heading: "Roboto Mono, monospace",
  },
  components: {
    Button: {
      baseStyle: {
        _focus: { boxShadow: "none" },
      },
    },
  },
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <App />
    </ChakraProvider>
  </React.StrictMode>
);
