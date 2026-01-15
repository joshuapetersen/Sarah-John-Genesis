import { useState, useEffect } from "react";
import { db } from "./firebase";
import { ref, onValue, push, serverTimestamp, query, limitToLast } from "firebase/database";

export default function useSovereignChat() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Listen to the last 50 messages
    const chatRef = query(ref(db, "sarah_chat_history"), limitToLast(50));

    const unsubscribe = onValue(chatRef, (snapshot) => {
      const data = snapshot.val();
      if (data) {
        // Convert object to array and sort by timestamp if needed (Firebase keys are chronological)
        const parsedMessages = Object.entries(data).map(([key, val]) => ({
          id: key,
          ...val
        }));
        setMessages(parsedMessages);
      } else {
        setMessages([]);
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const sendMessage = async (text, role = "user") => {
    const chatRef = ref(db, "sarah_chat_history");
    await push(chatRef, {
      role: role,
      content: text,
      timestamp: serverTimestamp()
    });
  };

  return { messages, loading, sendMessage };
}
