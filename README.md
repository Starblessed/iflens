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
  empty: No people visible in the scene.
  some: Some people visible in the scene.
  crowded: Lively scene crowded with lots of people.

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

---
### Attribution

- [Car Picture 1](examples\cars\domaxi198-shelby-3821712.jpg): Imagem de <a href="https://pixabay.com/pt/users/domaxi198-10651890/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=3821712">domaxi198</a> por <a href="https://pixabay.com/pt//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=3821712">Pixabay</a>
- [Car Picture 2](examples\cars\mrefraim1-car-2667246.jpg): Imagem de <a href="https://pixabay.com/pt/users/mrefraim1-6230354/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=2667246">mrefraim1</a> por <a href="https://pixabay.com/pt//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=2667246">Pixabay</a>
- [Car Picture 3](examples\cars\mibro-race-car-7624025.jpg): Imagem de <a href="https://pixabay.com/pt/users/mibro-8455312/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7624025">mibro</a> por <a href="https://pixabay.com/pt//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7624025">Pixabay</a>