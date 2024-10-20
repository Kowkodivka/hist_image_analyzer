import commonjs from '@rollup/plugin-commonjs'
import resolve from '@rollup/plugin-node-resolve'
import svelte from 'rollup-plugin-svelte'
import { sveltePreprocess } from 'svelte-preprocess'
import typescript from '@rollup/plugin-typescript'
import css from 'rollup-plugin-css-only'
import copy from 'rollup-plugin-copy'
import terser from '@rollup/plugin-terser'
import livereload from 'rollup-plugin-livereload'
import { spawn } from 'child_process'

const production = !process.env.ROLLUP_WATCH

function serve() {
  let server

  function toExit() {
    if (server) server.kill(0)
  }

  return {
    writeBundle() {
      if (server) return

      server = spawn('npm', ['run', 'start', '--', '--dev'], {
        stdio: ['ignore', 'inherit', 'inherit'],
        shell: true,
      })

      process.on('SIGTERM', toExit)
      process.on('exit', toExit)
    },
  }
}

export default {
  input: 'src/svelte/main.ts',
  output: {
    sourcemap: !production,
    format: 'iife',
    name: 'app',
    file: 'dist/public/build/bundle.js',
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
      output: 'bundle.css',
    }),
    copy({
      targets: [
        {
          src: 'src/svelte/public/**/*',
          dest: 'dist/public',
        },
      ],
    }),
    resolve({
      browser: true,
      dedupe: ['svelte'],
    }),
    commonjs(),
    typescript({
      tsconfig: 'src/svelte/tsconfig.json',
      sourceMap: !production,
      inlineSources: !production,
    }),
    !production && serve(),
    !production && livereload('dist'),
    production && terser(),
  ],
  watch: {
    clearScreen: false,
  },
}
