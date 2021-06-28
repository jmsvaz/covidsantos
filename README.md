# COVID-19 em Santos/SP

Os gráficos do site são minha tentativa de acompanhar a evolução da [COVID-19](https://pt.wikipedia.org/wiki/COVID-19) na cidade de [Santos/SP](https://pt.wikipedia.org/wiki/Santos), de acordo com as informações divulgadas pela Prefeitura de Santos.

O site oficial da [Prefeitura de Santos](https://egov.santos.sp.gov.br/santosmapeada/Saude/DadosDEVIG/MapaDEVIG/#) não divulga os dados dessa forma e ainda não existia quando comecei esse acompanhamento, de forma que resolvi produzi-los da maneira que acho mais conveniente.

## Script

Os dados divulgados no WhatsApp ou na conta da Prefeitura no [Instagram](https://www.instagram.com/santoscidade/) são compilados manualmente em um arquivo `csv` localizado na pasta `data` .

O script em python lê o arquivo `csv` e gera os gráficos no formato `svg`.

O site é hospedado no [GitHub](https://github.com/), sendo gerado pelo [Jekyll](https://jekyllrb.com/) e acessado pelo endereço <https://jmsvaz.github.io/covidsantos/>.

## Instalação

Para montar seu ambiente:

- Instale o Python 3 (testado em 3.9.5)
- Crie um virtualenv: `virtualenv env`
- Ative o virtualenv: `source env/bin/activate`
- Instale as dependências: `pip install -r requirements.txt`
- Rode o script: `./covidsantos.py`

A página inicial do site encontra-se em `docs` e os gráficos são gerados em `docs/img`.

## Fontes

- <https://www.instagram.com/santoscidade/>
- <https://commons.wikimedia.org/wiki/File:SARS-CoV-2_(CDC-23312).png>
