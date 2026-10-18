## Phạm Ngọc Trung

**AI Engineer** · Ho Chi Minh City, Vietnam

I build AI systems end to end: data, models, evaluation, inference, and the software people use them through.
For more than five years I have taken computer vision, Document AI and LLM applications from proof of concept to
production, and I build independent desktop products on FluentQt, the Python UI framework I created.

**What I work on**

- **LLMs, RAG and agents.** Agentic RAG, hybrid and graph retrieval, reranking, structured output, and local
  inference with Ollama, vLLM, SGLang and llama.cpp.
- **Document AI.** OCR, extraction with vision-language models, field localisation, validation and human review.
- **Computer vision and industrial AI.** Detection, segmentation, tracking and anomaly detection, connected to
  cameras, PLCs, Modbus, MQTT and edge devices.
- **Application engineering.** Python desktop software (PyQt5, FluentQt), FastAPI services, ONNX deployment and
  standalone builds.

### Independent products

The source of these projects is private. Each link opens a public showcase with documentation and screenshots.

- **[Veyra](https://github.com/pntrungbk15/veyra-showcase)**: a commercial machine-vision and AI inspection
  platform, developed since 2022. It has 72 vision and AI tools, camera and PLC stations, OK/NG evidence and
  labelling, and Ultralytics and Anomalib training with parity-checked ONNX exports (55 of 60 models verified end to
  end on CPU).
- **[Vietnamese Legal Intelligence](https://github.com/pntrungbk15/vietnamese-legal-intelligence-showcase)**: a legal
  research workstation. It parses 3,765 legal documents into more than 100,000 provisions and stores 120,000
  citations in a Neo4j knowledge graph. Hybrid retrieval combines BM25, multilingual E5 and rank fusion. Answers
  come from a local LLM, and each one is cited, checked against its sources, or declined.
- **[AI Annotation Workbench](https://github.com/pntrungbk15/annotation-workbench-showcase)**: computer-vision
  annotation with 16 local ONNX models across 11 tasks. It covers text-prompted and oriented detection, pose and OCR,
  plus video tracking, proposal review, and YOLO, COCO, DOTA and MOT export.
- **[ComicTranslator](https://github.com/pntrungbk15/comic-translator-showcase)**: local manga and comic
  translation. It detects bubbles, runs multilingual OCR, translates with a GGUF LLM through llama.cpp, then inpaints
  and letters each page for review.
- **[Fluent Data Studio](https://github.com/pntrungbk15/fluent-data-studio)**: AI-assisted data analysis. It turns
  natural-language requests into validated analysis plans, runs them on DuckDB, and produces editable charts and
  findings drawn from the computed results.
- **[FluentQt](https://github.com/pntrungbk15/fluentqt-showcase)**: a Fluent Design UI framework for PyQt5 in
  Community and Pro editions, maintained since 2022. Community has 177 widgets in 12 families, theming, frameless
  windows, six languages and SQLite persistence. Pro adds data grids, charts, a node editor and computer-vision UI.
  Every application above is built on it.

Also built on FluentQt: [Audio Story](https://github.com/pntrungbk15/audio-story-showcase), an AI audio-storytelling
studio, and [ChessForge](https://github.com/pntrungbk15/chessforge-showcase), a chess workstation with a PyTorch
self-play lab.

### Applied AI from industry work

These are independent re-implementations of systems I built professionally. They use synthetic data only and
contain no production code or customer data.

- **[SNY Septa Line Inspection](https://github.com/pntrungbk15/sny-septa-line-inspection)**: surface inspection of a
  coated technical knit with seven cameras.
- **[DocFlow IDP](https://github.com/pntrungbk15/docflow-idp)**: turns shipping-document PDFs into validated
  structured data, with a human-in-the-loop review workspace.
- **[Betty](https://github.com/pntrungbk15/betty-ai)**: an agentic RAG assistant that turns a conversation and a
  screenshot into a structured, estimated work ticket.
- **[ScanDoc AI](https://github.com/pntrungbk15/scandoc-ai)**: Document AI for scanned logistics documents. It
  reaches 88.9 % field accuracy on held-out synthetic scans.
- **[WebIntel Logistics](https://github.com/pntrungbk15/webintel-logistics)**: web crawling with layered
  structured extraction. It reaches 97.5 % field accuracy on held-out synthetic sites.
- **[T-Shirt Quality Inspection](https://github.com/pntrungbk15/tshirt-quality-in)** and
  **[Date Code Inspector](https://github.com/pntrungbk15/mfg-exp-reading)**: print and date-code inspection.

### Research implementations

Results and write-ups of detection models I implemented:
[YOLO](https://github.com/pntrungbk15/YOLO) (v1 to v11 and YOLOX),
[RYOLO](https://github.com/pntrungbk15/RYOLO) (oriented detection),
[YOLO-Seg](https://github.com/pntrungbk15/YOLO-Seg) (instance segmentation),
[EAST](https://github.com/pntrungbk15/An-Efficient-and-Accurate-Scene-Text-Detector) and
[CRAFT](https://github.com/pntrungbk15/Character-Region-Awareness-for-Text-Detection) (scene-text detection).

### Stack

- **ML and vision:** PyTorch, TensorFlow, ONNX Runtime, OpenCV, Ultralytics, Anomalib
- **LLM, VLM and RAG:** Gemini, Vertex AI, Ollama, vLLM, SGLang, llama.cpp, LoRA/QLoRA, pgvector, Neo4j
- **Software:** Python, C#, SQL, TypeScript; FastAPI, Flask, Django; PyQt5, PySide6, FluentQt; Next.js
- **Data:** PostgreSQL, SQLite, DuckDB, MongoDB, MinIO
- **Industrial and edge:** PLC integration, OPC UA, Modbus RTU/TCP, MQTT, ESP32, STM32, NVIDIA Jetson

### Background

M.Sc. and B.Eng. in Electrical and Electronics Engineering (Automation), Ho Chi Minh City University of Technology.

**Contact:** [pntrungbk15@gmail.com](mailto:pntrungbk15@gmail.com)
