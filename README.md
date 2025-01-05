# Image Analyzer with AI-Driven Suggestions

## Overview
This project is a Flask-based web application that uses **MobileNetV2** and **OpenAI's GPT-3.5** to analyze uploaded images and provide photography enhancement suggestions. It combines image recognition and AI-generated insights to help users improve their photography skills.

---

## Features
- **Image Upload and Analysis**: Users can upload an image, and the app will classify its primary scene or object using MobileNetV2.
- **AI-Powered Tips**: The app generates context-specific photography tips using OpenAI's GPT-3.5 model.
- **Dynamic Results**: Displays image analysis results along with improvement suggestions.
- **User-Friendly Interface**: Simple and clean UI for uploading images and viewing results.

---


---

## Requirements
- Python 3.8+
- TensorFlow
- Flask
- OpenAI Python SDK
- Pillow (for image processing)
- Dotenv (for environment variable management)

---
## Example Workflow

1. **Upload**: A user uploads an image of a sunset.

2. **Analysis**:
   - The app identifies the scene as "sunset."
   - GPT-3.5 suggests tips like:
     - "Use a tripod for stability during low light."
     - "Experiment with silhouette shots."

3. **Result**: The suggestions and the original image are displayed.


---

---
## Results

![Result Page Screenshot]("ss_scene_analyzer.png")

---

