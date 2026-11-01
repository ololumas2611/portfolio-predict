# Portfolio Predict

Extrator simples de histórico de dividendos da conta Trading 212 para um ficheiro CSV.

## Requisitos

- Python 3.10 ou superior
- Uma chave de API da Trading 212 com acesso ao histórico de dividendos
- O projeto utiliza chaves da conta live da trading 212

## Instalação

Clone o projeto e crie um ambiente virtual:

```bash
git clone <URL_DO_REPOSITORIO>
cd portfolio-predict
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
pip install requests python-dotenv
```

## Configuração

Crie um ficheiro `.env` na raiz do projeto:

```env
API_KEY=sua_chave_api
API_SECRET=seu_segredo_api
```

O ficheiro `.env` está incluído no `.gitignore` e não deve ser versionado. Nunca coloque chaves reais no README, no código ou em commits públicos.

## Execução

Com o ambiente virtual ativo, execute:

```bash
python data/01_raw.py
```

Por padrão, o resultado será gravado em `dividends.csv` na pasta atual. O programa percorre todas as páginas da API, aguarda entre chamadas e repete automaticamente chamadas que falhem por rate limit ou erros temporários do servidor.

Para alterar o caminho de saída, ajuste a chamada `get_data()` no ponto de entrada ou importe o módulo através de um carregador compatível com o nome de ficheiro `01_raw.py`.

## Formato do CSV

O CSV inclui os campos disponíveis do instrumento e os campos da operação, como:

- `currency`
- `amountInEuro`
- `paidOn`
- `type`
- `grossAmountPerShare`
- `reference`
- `quantity`
- `ticker`
- `name`
- `isin`
- `amount`

## Estrutura

```text
portfolio-predict/
├── core/
│   └── settings.py       # Configuração e credenciais
├── data/
│   └── 01_raw.py         # Extração da API Trading 212
├── service/
│   └── csv_service.py    # Escrita segura dos ficheiros CSV
├── .env                  # Credenciais locais; não versionar
└── README.md
```

## Validação local

Para verificar a sintaxe dos módulos:

```bash
python -m compileall -q core data service
```

O extrator só faz chamadas à API quando executado diretamente ou quando `get_data()` é chamado explicitamente.
