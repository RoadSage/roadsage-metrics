# Roadsage Metrics Website

Roadsage website for users to log in and view metrics from their device. It is a [Quasar](https://quasar.dev/) Vue framework application which compiles the application to a Single Page JavaScript application.

## Installation

Dependencies are managed using [npm](https://www.npmjs.com/).

```bash
npm install
```

## Linting

The code is formatted using the `prettier` formatter, to ensure consistency and readablility.
Most of the code is written using `typescript` to provide better editor experience and catch errors.
`eslint` is used to pick up on various errors, and lint the code.

```bash
npm run lint
npm run format
```

## Usage

### Link to the Backend

All requests in the application will be made to the backend API at an address specified at the top of ./frontend/src/boot/axios.ts.

The typical development enviroment will have the fastAPI backend running at: 'http://localhost:8000'. When deployed to a server, the backend API will be running at a different address and this variable needs to be updated to have the appropriate address.

### Start the app in development mode (hot-code reloading, error reporting, etc.)

```bash
npm run dev
```

### Build for Production

```bash
npm run build
```

The application is built into the /frontend/dist/spa directory. This directory can be hosted on a static site server such as Vercel, Netlify, GitHub pages, or similar.
