from __future__ import annotations

import os
from dataclasses import dataclass

from huggingface_hub import hf_hub_download
from llama_cpp import Llama


@dataclass
class ModelConfig:
    repo_id: str = os.getenv("HF_REPO_ID", "bartowski/Qwen2.5-0.5B-Instruct-GGUF")
    filename: str = os.getenv("HF_FILENAME", "Qwen2.5-0.5B-Instruct-Q4_K_M.gguf")
    n_ctx: int = int(os.getenv("LLM_N_CTX", "1024"))
    n_threads: int = int(os.getenv("LLM_N_THREADS", "4"))
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))


def load_model(config: ModelConfig | None = None) -> Llama:
    cfg = config or ModelConfig()
    model_path = hf_hub_download(repo_id=cfg.repo_id, filename=cfg.filename)
    llm = Llama(
        model_path=model_path,
        n_ctx=cfg.n_ctx,
        n_threads=cfg.n_threads,
        verbose=False,
    )
    return llm


def generate(llm: Llama, prompt: str, temperature: float = 0.3, max_tokens: int = 256) -> str:
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "Tu es un assistant d'automatisation local, précis et prudent."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response["choices"][0]["message"]["content"].strip()
