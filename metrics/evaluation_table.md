# 📊 Evaluation Metrics

| Strategy                |   Question_Macro_F1 |   Statement_Macro_F1 |   Statement_Evidence_Macro_F1 |   Reasoning_F1 |
|:------------------------|--------------------:|---------------------:|------------------------------:|---------------:|
| baseline                |              0.2072 |               0.1925 |                        0.0182 |         0.0182 |
| initial_strategy        |              0.7526 |               0.4015 |                        0.1849 |         0.1405 |
| deepseek_benchmark      |              0.476  |               0.1157 |                        0.0445 |         0.0362 |
| reward_reranking        |              0.7658 |               0.366  |                        0.1041 |         0.0439 |
| joint_verifier_strategy |              0.7253 |               0.2152 |                        0.0953 |         0.0681 |
| hybrid_strategy_v1      |              0.7781 |               0.4007 |                        0.1276 |         0.088  |
| hybrid_strategy_v2      |              0.7658 |               0.4102 |                        0.1711 |         0.1231 |
| hybrid_strategy_v3      |              0.7658 |               0.399  |                        0.1831 |         0.1129 |
| hybrid_strategy_v4      |              0.7658 |               0.4185 |                        0.1214 |         0.0939 |