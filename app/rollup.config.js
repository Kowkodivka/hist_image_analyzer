import commonjs from "@rollup/plugin-commonjs";
import resolve from "@rollup/plugin-node-resolve";
import svelte from "rollup-plugin-svelte";
import { sveltePreprocess } from "svelte-preprocess";
import typescript from "@rollup/plugin-typescript";
import css from "rollup-plugin-css-only";
import copy from "rollup-plugin-copy";
import terser from "@rollup/plugin-terser";
import livereload from "rollup-plugin-livereload";
import { spawn } from "child_process";

const production = !process.env.ROLLUP_WATCH;

function serve() {
  let server;

  function exit() {
    if (server) server.kill(0);
  }

  return {
    writeBundle() {
      if (server) return;

      server = spawn("npm", ["run", "start", "--", "--dev"], {
        stdio: ["ignore", "inherit", "inherit"],
        shell: true,
      });

      process.on("SIGTERM", exit);
      process.on("exit", exit);
    },
  };
}

export default {
  input: "src/frontend/main.ts",
  output: {
    sourcemap: !production,
    format: "iife",
    name: "app",
    file: "dist/www/build/bundle.js",
  },
  plugins: [
    svelte({
      preprocess: sveltePreprocess({
        sourceMap: !production,
      }),
      compilerOptions: {
        dev: !production,
      },
    }),
    css({
      output: "bundle.css",
    }),
    copy({
      targets: [
        {
          src: "src/frontend/www/**/*",
          dest: "dist/www",
        },
      ],
    }),
    resolve({
      browser: true,
      dedupe: ["svelte"],
    }),
    commonjs(),
    typescript({
      tsconfig: "src/frontend/tsconfig.json",
      sourceMap: !production,
      inlineSources: !production,
    }),
    !production && serve(),
    !production && livereload("dist"),
    production && terser(),
  ],
  watch: {
    clearScreen: false,
  },
};
