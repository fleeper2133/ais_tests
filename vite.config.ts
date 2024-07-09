import { defineConfig } from "vite";
import { resolve } from "path";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  css: {
    preprocessorOptions: {
      
    }
  },
  root: resolve("./app/static/src"),
  base: "/static/",
  plugins: [vue()],
  build: {
    outDir: resolve("./app/static/dist"),
    assetsDir: "",
    manifest: 'manifest.json',
    emptyOutDir: true,
    rollupOptions: {
      // Overwrite default .html entry to main.ts in the static directory
      input: resolve("./app/static/src/main.ts"),
    },
  },
  server: {
    hmr: {
        host: 'localhost',
    },
}
});
