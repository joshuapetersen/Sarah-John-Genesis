import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";
import { getFirestore } from "firebase/firestore";

// Sovereign Genesis Bridge Configuration
// Project ID: genesis-fd692 (User Provided)
const firebaseConfig = {
  apiKey: "AIzaSyDOC-PLACEHOLDER-KEY-FOR-GENESIS-BRIDGE", // Placeholder until user provides API Key
  authDomain: "genesis-fd692.firebaseapp.com",
  databaseURL: "https://genesis-fd692-default-rtdb.firebaseio.com",
  projectId: "genesis-fd692",
  storageBucket: "genesis-fd692.appspot.com",
  messagingSenderId: "1092777037037", // Resonance derived ID (placeholder)
  appId: "1:1092777037037:web:genesis_bridge_id"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Services
export const db = getDatabase(app);
export const firestore = getFirestore(app);

console.log("[Sovereign Bridge] Firebase Initialized for Genesis-FD692");
