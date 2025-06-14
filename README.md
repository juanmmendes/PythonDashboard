# 📊 Dashboard de Vendas Estratégico

Um painel interativo construído com **Streamlit** + **Plotly** que transforma dados (mesmo que fictícios!) em insights visuais de forma rápida e elegante.

> “Prototipar não precisa demorar — algumas linhas de Python já viram produto.”

## ✨ Funcionalidades

- **Geração de dados simulados** com `pandas`, `numpy` e um toque de aleatoriedade.
- **Filtros inteligentes** (Ano, Categoria, Região, Vendedor) diretamente na sidebar.
- **KPIs em tempo real** mostrando Receita, Lucro, Volume de Vendas, Ticket Médio e Margem.
- **Gráficos interativos** de linha, pizza, barras e heatmap usando Plotly.
- **Insights estratégicos automáticos** (produto campeão, região destaque, etc.).
- Design responsivo e temas leves com CSS customizado.

## 🛠️ Tecnologias & Bibliotecas

| Camada | Tecnologias |
|--------|-------------|
| Front‑end / UI | **Streamlit** 1.x, HTML/CSS in‑app |
| Visualização | **Plotly Express & Graph Objects** |
| Back‑end (Python) | `pandas`, `numpy`, `datetime`, `random` |
| Ambiente | Python 3.10+, virtualenv/conda |

## 🚀 Instalação Rápida

```bash
# clone o repositório
git clone https://github.com/seu-usuario/dashboard-vendas.git
cd dashboard-vendas

# crie ambiente e instale dependências
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# rode o app
streamlit run dashboard.py
```

> Dica: se quiser testar sem clonar, experimente [Streamlit Cloud](https://streamlit.io/cloud) e suba direto do GitHub.

## 🔧 Personalização

- **Dados reais:** substitua a função `generate_sales_data()` por seu DataFrame.
- **KPIs:** altere `calcular_metricas()` para refletir métricas do seu negócio.
- **Estilo:** ajuste o CSS embutido ou use o novo tema configurável do Streamlit.

## 🤝 Contribuindo

1. Faça um fork.
2. Crie uma branch: `git checkout -b feat/nova-funcionalidade`
3. Commit suas alterações: `git commit -m 'feat: minha feature'`
4. Push: `git push origin feat/nova-funcionalidade`
5. Abra um Pull Request 🙌

## 📜 Licença

MIT – faça bom uso, gere insights e compartilhe conhecimento!

---
_Dashboard desenvolvido por [Seu Nome] • Dados 100% fictícios para fins de demonstração_