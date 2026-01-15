import { useState, useEffect } from "react";
import { db } from "./firebase";
import { ref, onValue } from "firebase/database";

export default function useSovereignData(path = "system_metrics/heartbeat") {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Reference to the Sovereign Data Path
    const sovereignRef = ref(db, path);

    // Listen for Real-Time Changes
    const unsubscribe = onValue(sovereignRef, (snapshot) => {
      const val = snapshot.val();
      if (val) {
        setData(val);
      } else {
        setData(null); // No data yet
      }
      setLoading(false);
    }, (err) => {
      console.error("[Sovereign Bridge] Sync Error:", err);
      setError(err);
      setLoading(false);
    });

    // Cleanup Listener on Unmount
    return () => unsubscribe();
  }, [path]);

  return { data, loading, error };
}
