"""Local-only Gradio interface."""

from __future__ import annotations

import time
from pathlib import Path

import gradio as gr
import pandas as pd

from src.recommender import HybridRecommender


def build_demo(recommender: HybridRecommender) -> gr.Blocks:
    def search(query: str) -> tuple[pd.DataFrame, str]:
        started = time.perf_counter()
        rows = recommender.recommend(query, k=5)
        elapsed_ms = (time.perf_counter() - started) * 1000
        table = pd.DataFrame(rows)
        status = f"Inférence : {elapsed_ms:.1f} ms · device : {recommender.device}"
        return table, status

    with gr.Blocks(title="Xbox Search Recommender") as demo:
        gr.Markdown("# Xbox Search Recommender\nMoteur hybride exécuté entièrement en local.")
        query = gr.Textbox(label="Requête", placeholder="Ex. space shooter, racing game…")
        submit = gr.Button("Rechercher", variant="primary")
        results = gr.Dataframe(label="Top 5", interactive=False)
        status = gr.Markdown()
        gr.Examples(
            examples=[["halo"], ["fast car game"], ["pirate adventure"]], inputs=query
        )
        submit.click(search, inputs=query, outputs=[results, status])
        query.submit(search, inputs=query, outputs=[results, status])
    return demo


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    recommender = HybridRecommender(root / "artifacts")
    demo = build_demo(recommender)
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)


if __name__ == "__main__":
    main()

