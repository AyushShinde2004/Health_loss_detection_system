# 🩺 Health Bar OCR Monitor

This Python script monitors the health bar in a game using Optical Character Recognition (OCR). By capturing a specified region of the screen, it detects health changes in real time, providing insights into in-game health status.

---

## 🚀 Features:

- 📸 **Screen Capture**: Captures a customizable region of the screen to focus on the health bar.
- 🔍 **Advanced OCR**: Uses EasyOCR to extract numeric values from the health bar image.
- 📉 **Health Tracking**: Monitors and logs health changes, including detecting health loss.
- ⏱️ **Real-Time Analysis**: Processes health bar updates continuously with minimal delay.
- 🛑 **User-Friendly Controls**: Allows safe interruption via keyboard or GUI.
- ⚙️ **Customizable Settings**: Easily configure the region, OCR language, and other parameters.
- 🖥️ **Visualization**: Displays the captured health bar region in a real-time window.

---

## 🛠️ Requirements

Before running the script, ensure you have the following dependencies installed:

```bash
pip install opencv-python-headless easyocr pyautogui numpy
```

---

## 📂 Description

This script is designed for gamers and developers who need to monitor health bars or other screen elements dynamically. It uses:

- **PyAutoGUI** for screen capturing.
- **OpenCV** for image processing.
- **EasyOCR** for text recognition.

### How It Works:
1. Define the screen region containing the health bar.
2. Capture the region at regular intervals.
3. Process the captured image to extract text.
4. Compare the extracted health value with the previous value to detect changes.
5. Display the captured region in a window for real-time visualization.

---

## ⚙️ Configuration

- **Health Bar Region**: Update the `health_bar_region` coordinates to align with your screen setup.
  ```python
  health_bar_region = (1993, 414, 200, 220)
  ```

- **OCR Language**: Modify the language settings for OCR based on your needs.
  ```python
  reader = easyocr.Reader(['en'], gpu=True)
  ```

- **Monitoring Frequency**: Adjust the `time.sleep()` interval for faster or slower monitoring.

---


## 👩‍💻 Contributing
Feel free to submit issues or pull requests to improve this script.

---

## 📜 License
This project is licensed under the MIT License. See the `LICENSE` file for details.
