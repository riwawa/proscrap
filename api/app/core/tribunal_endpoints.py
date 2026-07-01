# Mapeamento de tribunais para endpoints da API Pública DataJud (CNJ)
# Fonte: Tutorial oficial CNJ (DPJ) - tutorial-api-publica-datajud-beta.pdf
# Total: 91 tribunais
# Base URL: https://api-publica.datajud.cnj.jus.br/{alias}/_search

from app.core.config import get_settings

settings = get_settings()
BASE_URL = settings.datajud_base_url

TRIBUNAL_ENDPOINTS: dict[str, str] = {
    # Tribunais Superiores
    "tst": f"{BASE_URL}/api_publica_tst/_search",
    "tse": f"{BASE_URL}/api_publica_tse/_search",
    "stj": f"{BASE_URL}/api_publica_stj/_search",
    "stm": f"{BASE_URL}/api_publica_stm/_search",

    # Justiça Federal
    "trf1": f"{BASE_URL}/api_publica_trf1/_search",
    "trf2": f"{BASE_URL}/api_publica_trf2/_search",
    "trf3": f"{BASE_URL}/api_publica_trf3/_search",
    "trf4": f"{BASE_URL}/api_publica_trf4/_search",
    "trf5": f"{BASE_URL}/api_publica_trf5/_search",
    "trf6": f"{BASE_URL}/api_publica_trf6/_search",

    # Justiça Estadual
    "tjac": f"{BASE_URL}/api_publica_tjac/_search",
    "tjal": f"{BASE_URL}/api_publica_tjal/_search",
    "tjam": f"{BASE_URL}/api_publica_tjam/_search",
    "tjap": f"{BASE_URL}/api_publica_tjap/_search",
    "tjba": f"{BASE_URL}/api_publica_tjba/_search",
    "tjce": f"{BASE_URL}/api_publica_tjce/_search",
    "tjdft": f"{BASE_URL}/api_publica_tjdft/_search",
    "tjes": f"{BASE_URL}/api_publica_tjes/_search",
    "tjgo": f"{BASE_URL}/api_publica_tjgo/_search",
    "tjma": f"{BASE_URL}/api_publica_tjma/_search",
    "tjmg": f"{BASE_URL}/api_publica_tjmg/_search",
    "tjms": f"{BASE_URL}/api_publica_tjms/_search",
    "tjmt": f"{BASE_URL}/api_publica_tjmt/_search",
    "tjpa": f"{BASE_URL}/api_publica_tjpa/_search",
    "tjpb": f"{BASE_URL}/api_publica_tjpb/_search",
    "tjpe": f"{BASE_URL}/api_publica_tjpe/_search",
    "tjpi": f"{BASE_URL}/api_publica_tjpi/_search",
    "tjpr": f"{BASE_URL}/api_publica_tjpr/_search",
    "tjrj": f"{BASE_URL}/api_publica_tjrj/_search",
    "tjrn": f"{BASE_URL}/api_publica_tjrn/_search",
    "tjro": f"{BASE_URL}/api_publica_tjro/_search",
    "tjrr": f"{BASE_URL}/api_publica_tjrr/_search",
    "tjrs": f"{BASE_URL}/api_publica_tjrs/_search",
    "tjsc": f"{BASE_URL}/api_publica_tjsc/_search",
    "tjse": f"{BASE_URL}/api_publica_tjse/_search",
    "tjsp": f"{BASE_URL}/api_publica_tjsp/_search",  # foco v1
    "tjto": f"{BASE_URL}/api_publica_tjto/_search",

    # Justiça do Trabalho
    "trt1": f"{BASE_URL}/api_publica_trt1/_search",
    "trt2": f"{BASE_URL}/api_publica_trt2/_search",
    "trt3": f"{BASE_URL}/api_publica_trt3/_search",
    "trt4": f"{BASE_URL}/api_publica_trt4/_search",
    "trt5": f"{BASE_URL}/api_publica_trt5/_search",
    "trt6": f"{BASE_URL}/api_publica_trt6/_search",
    "trt7": f"{BASE_URL}/api_publica_trt7/_search",
    "trt8": f"{BASE_URL}/api_publica_trt8/_search",
    "trt9": f"{BASE_URL}/api_publica_trt9/_search",
    "trt10": f"{BASE_URL}/api_publica_trt10/_search",
    "trt11": f"{BASE_URL}/api_publica_trt11/_search",
    "trt12": f"{BASE_URL}/api_publica_trt12/_search",
    "trt13": f"{BASE_URL}/api_publica_trt13/_search",
    "trt14": f"{BASE_URL}/api_publica_trt14/_search",
    "trt15": f"{BASE_URL}/api_publica_trt15/_search",
    # NOTA: o anexo oficial do tutorial CNJ lista "trt15" duas vezes (15ª e 16ª regiao),
    # provável typo. Mantido como trt16 por inferência -> CONFIRMAR no S0 com chamada real.
    "trt16": f"{BASE_URL}/api_publica_trt16/_search",
    "trt17": f"{BASE_URL}/api_publica_trt17/_search",
    "trt18": f"{BASE_URL}/api_publica_trt18/_search",
    "trt19": f"{BASE_URL}/api_publica_trt19/_search",
    "trt20": f"{BASE_URL}/api_publica_trt20/_search",
    "trt21": f"{BASE_URL}/api_publica_trt21/_search",
    "trt22": f"{BASE_URL}/api_publica_trt22/_search",
    "trt23": f"{BASE_URL}/api_publica_trt23/_search",
    "trt24": f"{BASE_URL}/api_publica_trt24/_search",

    # Justiça Eleitoral
    "tre-ac": f"{BASE_URL}/api_publica_tre-ac/_search",
    "tre-al": f"{BASE_URL}/api_publica_tre-al/_search",
    "tre-am": f"{BASE_URL}/api_publica_tre-am/_search",
    "tre-ap": f"{BASE_URL}/api_publica_tre-ap/_search",
    "tre-ba": f"{BASE_URL}/api_publica_tre-ba/_search",
    "tre-ce": f"{BASE_URL}/api_publica_tre-ce/_search",
    "tre-df": f"{BASE_URL}/api_publica_tre-df/_search",
    "tre-es": f"{BASE_URL}/api_publica_tre-es/_search",
    "tre-go": f"{BASE_URL}/api_publica_tre-go/_search",
    "tre-ma": f"{BASE_URL}/api_publica_tre-ma/_search",
    "tre-mg": f"{BASE_URL}/api_publica_tre-mg/_search",
    "tre-ms": f"{BASE_URL}/api_publica_tre-ms/_search",
    "tre-mt": f"{BASE_URL}/api_publica_tre-mt/_search",
    "tre-pa": f"{BASE_URL}/api_publica_tre-pa/_search",
    "tre-pb": f"{BASE_URL}/api_publica_tre-pb/_search",
    "tre-pe": f"{BASE_URL}/api_publica_tre-pe/_search",
    "tre-pi": f"{BASE_URL}/api_publica_tre-pi/_search",
    "tre-pr": f"{BASE_URL}/api_publica_tre-pr/_search",
    "tre-rj": f"{BASE_URL}/api_publica_tre-rj/_search",
    "tre-rn": f"{BASE_URL}/api_publica_tre-rn/_search",
    "tre-ro": f"{BASE_URL}/api_publica_tre-ro/_search",
    "tre-rr": f"{BASE_URL}/api_publica_tre-rr/_search",
    "tre-rs": f"{BASE_URL}/api_publica_tre-rs/_search",
    "tre-sc": f"{BASE_URL}/api_publica_tre-sc/_search",
    "tre-se": f"{BASE_URL}/api_publica_tre-se/_search",
    "tre-sp": f"{BASE_URL}/api_publica_tre-sp/_search",
    "tre-to": f"{BASE_URL}/api_publica_tre-to/_search",

    # Justiça Militar
    "tjmmg": f"{BASE_URL}/api_publica_tjmmg/_search",
    "tjmrs": f"{BASE_URL}/api_publica_tjmrs/_search",
    "tjmsp": f"{BASE_URL}/api_publica_tjmsp/_search",
}

# Mapeamento código J.TR (segmento.tribunal) do número CNJ -> alias do tribunal.
# PENDENTE (decisão tomada: deixar para depois do S0).
# Fonte a consultar: Resolução CNJ nº 65/2008 (tabela de codificação dos órgãos
# do Poder Judiciário) — não vem no tutorial da API pública.
# Só os pares abaixo foram confirmados nesta sessão de design; o restante deve
# ser populado e validado no S1.
CNJ_SEGMENTO_TRIBUNAL_PARA_ALIAS: dict[str, str] = {
    "8.26": "tjsp",
    "8.04": "tjam",
    # TODO (S1): completar a partir da Resolução CNJ 65/2008.
}


def resolver_alias_por_numero_cnj(numero_cnj: str) -> str | None:
    """
    Resolve o alias do tribunal a partir do número de processo no padrão CNJ
    (NNNNNNN-DD.AAAA.J.TR.OOOO). Retorna None se o segmento J.TR não estiver
    mapeado ainda (ver TODO acima).

    Esta função é um placeholder estrutural — a tabela completa ainda não
    está populada (decisão: fechar depois do spike S0).
    """
    partes = numero_cnj.replace("-", ".").split(".")
    if len(partes) < 5:
        return None
    j, tr = partes[3], partes[4]
    chave = f"{j}.{tr}"
    return CNJ_SEGMENTO_TRIBUNAL_PARA_ALIAS.get(chave)
