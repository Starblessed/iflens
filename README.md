# iflens - Ferramenta de Aumento de Dados com IA Generativa
![Static Badge](https://img.shields.io/badge/Gemini-OK-green?logo=googlegemini) ![Static Badge](https://img.shields.io/badge/Groq-OK-green?logo=groq) ![Static Badge](https://img.shields.io/badge/OpenAI-WIP-yellow?logo=openai) ![Static Badge](https://img.shields.io/badge/Claude-TODO-black?logo=claude)


## Instalação

### Clone o repositório
```bash
git clone https://github.com/Starblessed/iflens.git .
```

### Instale as dependências

uv (recomendado)
```bash
uv sync
```
python
```bash
python -m venv .venv

.venv\Scripts\activate # Windows
.venv\bin\activate # Linux

pip install .
```

## Utilização

### Configuração de Condições

Edite o arquivo `conditions-example.yaml` com as condições desejadas para classificação das imagens.

```yaml
people:
  empty: Clean atmosphere without visible fog.
  some: Light mist diffused across the scene.
  crowded: Thick fog atmosphere with object occlusion.

time_of_day:
  dawn: Early daylight with low ambient illumination.
  morning: Morning daylight with moderate illumination.
  noon: Bright overhead daylight with strong illumination.
  afternoon: Afternoon daylight with warm angled illumination.
  dusk: Fading daylight with low ambient illumination.
  night: Nighttime with minimal natural illumination.

precipitation:
  clean: No precipitation.
  light_rain: Light rainfall with minor visibility reduction.
  heavy_rain: Heavy rainfall with significant visibility reduction.
  stormfront: Severe storm with intense rainfall and turbulent conditions.
  snow: Light snowfall with minor visibility reduction.
  heavy_snow: Heavy snowfall with significant visibility reduction.
  blizzard: Severe snowfall with strong winds and low visibility.

planet:
  earth: Stardard picture taken on planet Earth.
  mars: Picture taken on planet Mars.
```

### Chaves de API
Faça uma cópia do arquivo `.env.example`, renomeie-o para `.env` e preencha os campos com as chaves de API solicitadas:

```ini
GEMINI_API_KEY=YOUR_KEY_HERE
GROQ_API_KEY=YOUR_KEY_HERE
```

### Configurações de Pipeline

Altere as variáveis de geração no script `iflens/main.py`

```python
NUMBER_OF_SAMPLE_IMAGES: int = 1 # Should be equal or smaller than the dataset size

DATASET_PATH: str = os.path.join("examples", "street")
CONDITIONS_YAML_FILE: str = "conditions-example.yaml"

KEEP_CLASSES: list[str] = ["planet"] # Prevents the tool from varying specific condition classes

GENERATION_MODEL: str = "gemini-3.1-flash-lite-image"
```

### Execução
Abra um console na pasta raiz e execute:

uv (recomendado)
```bash
uv run python -m iflens.main
```

python
```bash
.venv\Scripts\activate # Windows
.venv\bin\activate # Linux

python -m iflens.main
```