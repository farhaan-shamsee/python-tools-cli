# PYTHON TOOLS CLI

## Usage

```python
# Version command
python cli.py version

# Cluster commands
python cli.py cluster create my-cluster --provider local --ports 80,443 --registry
python cli.py cluster delete my-cluster --provider local
python cli.py cluster list --provider aws
python cli.py cluster info my-cluster --provider local
python cli.py cluster bootstrap my-cluster --provider local

# Tools commands
python cli.py tools list
python cli.py tools install kubectl helm
python cli.py tools check kubectl

# Config commands
python cli.py config init --output my-config.yaml
python cli.py config show --config-path config.yaml
python cli.py config validate --config-path config.yaml
```