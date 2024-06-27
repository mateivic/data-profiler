import React from "react";
import { createBrowserRouter } from "react-router-dom";
import CredentialsForm from "./pages/CredentialsForm";
import Results from "./pages/Results";


export const routes = [
    { path: "/", element: <CredentialsForm /> },
    { path: "/results", element: <Results /> },
];

export const router = createBrowserRouter(routes);
