# 🌟 GlowingPy

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/) [![License](https://img.shields.io/badge/license-MIT-green)](LICENSE) [![GitHub stars](https://img.shields.io/github/stars/FERNAN19898/glowing-py?style=social)](https://github.com/FERNAN19898/glowing-py/stargazers)

**GlowingPy** is a dynamic LED strip controller that reacts to games, music, and custom choreography. Your LEDs now **dance, flash, and react in real-time**.

---

## 🎮 Planned compatible games and effects

| ID | Game | Mode | Description | Status |
|----|------|------|-------------|--------|
| X | Friday Night Funkin' | Key Sync | LEDs react to **D, F, J, K** inputs | 🛠️ In progress |
| X | Left 4 Dead 2 | Health Bar | Visualizes player health on LEDs | 🛠️ In progress |
| X | Left 4 Dead 2 | Special Events | LED orchestration for **Tank / Special Infected** | 🛠️ In progress |
| X | Portal 2 | Portal Tracker | LED color shows **last portal placed** | 🛠️ In progress |
| X | Custom Songs | Choreography | Detect song via Stereo Mix & sync LED sequences | 🛠️ In progress |

More in the future!

---

## ⚡ Features

- Plugin-based system: add new effects easily  
- Real-time LED feedback for games and music  
- Supports WLED-controlled LED strips  
- Custom choreography files (`fseq`) for music  
- Simple keyboard shortcuts: **F7 to stop plugins**  

---

## 🎬 Demo (Example)

![GlowingPy Demo](https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif)  

*LEDs reacting to a song and in-game events.*

---

## 🛠 Installation

```bash
git clone https://github.com/FERNAN19898/glowing-py.git
cd glowing-py
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Configure your WLED device in `config.json`:

```json
{
    "wled_ip": "192.168.1.100",
    "wled_port": 80,
    "led_count": 60
}
```

---

## 🚀 Usage

Run the main engine:

```
python main.py
```

- Select a plugin or view available ones  
- Press **F7** to stop any running plugin  
- Extend functionality by creating your own plugin  

---

## 📂 Plugin Structure

```
plugins/
└── my_plugin/
    ├── my_plugin.py   # Plugin class with run() coroutine
    └── README.md      # Optional info
```

Each plugin must implement:

```python
from ..base_plugin import BasePlugin

class Plugin(BasePlugin):
    """
    Example Plugin Template.
    Copy this folder and rename it to create a new plugin.
    """

    async def setup(self) -> None:
        """
        Called once when the plugin starts.
        Initialize variables or states here.
        """
        pass

    async def loop(self) -> None:
        """
        Called repeatedly while the plugin is running.
        Implement animation logic here.
        """
        pass

    async def on_plugin_stopped(self) -> None:
        """
        Called once when the plugin stops.
        Use this to reset LEDs or cleanup tasks.
        """
        pass
```
See plugins/_template/_template.py for more inforamtion!

---

## 💡 Contributing

- Add new game integrations or effects  
- Optimize LED animations  
- Share your custom choreography files  

---

## 📝 License

This project is **MIT Licensed**.
