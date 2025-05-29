const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log("MongoDB Connected"))
.catch(err => console.error("MongoDB connection error:", err));

// User Schema & Model
const userSchema = new mongoose.Schema({
  name: String,
  email: { type: String, unique: true },
  progress: Object,
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

// Routes

// Test route
app.get('/', (req, res) => {
  res.send("CyberDrake Backend is running!");
});

// Submit quiz / progress update
app.post('/submit_quiz', async (req, res) => {
  const { email, answers } = req.body;
  try {
    // Save or update user progress
    const user = await User.findOneAndUpdate(
      { email },
      { $set: { progress: answers } },
      { upsert: true, new: true }
    );
    res.json({ status: "success", user });
  } catch (error) {
    console.error("Error updating user progress:", error);
    res.status(500).json({ status: "error", error: error.message });
  }
});

// Get all users - For admin dashboard
app.get('/admin/users', async (req, res) => {
  try {
    const users = await User.find({}, 'email progress');
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch user data' });
  }
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
