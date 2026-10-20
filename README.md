# Guardian Calculation Assistant (GCA)

Mod de interface para **Crusader Kings III** que ajuda a escolher o guardião de uma criança. Cada candidato da lista ganha uma nota com a chance real de progresso na educação, calculada com a mesma fórmula que o jogo usa.

Inspirado no Marriage Calculation Assistant (MCA), que faz o mesmo para casamentos.

*English summary at the end.*

## O que o mod faz

### Nota GCA em cada candidato

Nas listas de **Educar a Criança**, **Oferecer Tutela** e **Oferecer Pupilo**, cada linha mostra:

```
GCA 64% ~R3
```

- **64%**: chance de a criança ganhar +2 pontos de educação a cada aniversário (dos 6 aos 15 anos) com esse guardião.
- **~R3**: nível de educação projetado ao chegar à maioridade (só aparece quando a criança já tem foco de educação).

Passe o mouse para ver o detalhamento:

- peso de progresso e peso de falha, com cada fator separado;
- projeção de pontos: pontos atuais + aniversários restantes × 2 × chance;
- avisos que se aplicam ao par: Sinalização da aprendizagem, Pedagogia, transferência de traço de comandante, Cavalaria, fé ou cultura diferentes.

A nota funciona nos dois sentidos. Com a criança escolhida, avalia os guardiões. Com o guardião escolhido, avalia as crianças.

### Procurar guardião fora da sua corte

O vanilla só deixa escolher guardiões da sua própria corte (ou da corte de um governante específico). O GCA adiciona a interação **Procurar guardião (GCA)** no menu de qualquer criança da sua corte sem guardião. Ela lista:

- você e seus cortesãos;
- todos os governantes no seu alcance diplomático e os cortesãos deles.

Ao escolher um candidato e clicar em **Continuar**, o mod abre a interação vanilla correta já preenchida:

- **Educar a Criança**, se o guardião é da sua corte;
- **Oferecer Pupilo** ao governante do guardião, se ele é de fora.

Custos, validade e aceitação continuam sendo os do vanilla.

### Ordenar por nota

Na busca GCA a lista já abre ordenada pela maior nota. Abaixo do dropdown de ordenação nativo (que continua disponível) ficam dois botões:

- **GCA: por nota**: ordena pela chance GCA, da maior para a menor;
- **Lista padrão**: volta para a ordem do jogo.

A ordenação se desfaz se a lista mudar, se o dia do jogo avançar com a janela aberta ou se o painel de filtros nativo estiver aberto. É só clicar em "GCA: por nota" de novo.

### Filtro de inteligência

Checkboxes **Rápido / Inteligente / Genial** acima da lista mostram só quem tem os traços marcados (sem nada marcado, mostra todos). Vale para guardiões e pupilos. O filtro nativo de **Traços** também foi adicionado ao painel de filtros.

## Como a nota é calculada

O GCA reproduz `education_point_acquisition_support_effect` (`common/scripted_effects/00_education_effects.txt`, CK3 1.19). A cada aniversário dos 6 aos 15 anos o jogo sorteia entre:

| Progresso (+2 pontos no foco) | Peso |
|---|---|
| Base | 60 |
| Inteligência da criança: Genial / Inteligente / Rápido ou Astuto | +20 / +15 / +10 |
| Traço de infância compatível / incompatível com o foco | +20 / -20 |
| Inteligência do guardião: Genial / Inteligente / Rápido ou Astuto | +15 / +10 / +5 |
| Habilidade do guardião no foco | × 0,4 |
| Erudição do guardião | × 0,2 |
| Aspiração de casa do guardião (melhor resultado de educador) | +5 |

| Sem progresso | Peso |
|---|---|
| Base | 40 |
| Criança: Imbecil ou Endogamia / Estúpido / Devagar ou Maçante | +20 / +15 / +10 |
| Guardião: Imbecil / Estúpido / Devagar ou Maçante | +15 / +10 / +5 |

**Chance = progresso / (progresso + sem progresso).**

Detalhes fiéis ao vanilla:

- **Culturas com "melhor educação de pupilos"** (Contadores de histórias e similares): por causa de como o script vanilla foi escrito, essas culturas *substituem* o bônus de inteligência e habilidade do guardião por +10 fixo, em vez de somar. O GCA reproduz isso e avisa no tooltip.
- **Criança sem foco ainda**: o GCA considera a melhor habilidade do guardião.
- **Nível projetado**: usa os cortes vanilla `education_level_1/2/3` (7/12/17 pontos). `~R4` significa nível 4 ou 5 (o 5 depende de bônus de dinastia ou propriedade).
- **Sinalização da aprendizagem** (Beacon of Learning) na cultura do guardião soma `arredondar(pontos/4)`, até +3, na maioridade. Isso entra na projeção.

A projeção conta só essas rolagens de aniversário. Eventos, tutores da corte, universidades e outras fontes podem somar mais.

Os multiplicadores são lidos dos script values do próprio jogo (`educator_skill_modifier_factor`, `matching_childhood_trait_modifier_value` etc.). Mods que mudam esses valores são respeitados automaticamente.

## Instalação

1. Baixe o `guardian_calc_assistant-<versão>.zip` na página de **Releases**.
2. Extraia dentro de `Documentos/Paradox Interactive/Crusader Kings III/mod/`. Devem ficar lado a lado:

   ```
   mod/
     guardian_calc_assistant.mod
     guardian_calc_assistant/
   ```

3. Ative o mod no launcher.

Compatível com saves existentes. Pode ser removido a qualquer momento: as únicas variáveis gravadas no save são o filtro de inteligência e a ordenação, ambas no seu personagem.

## Compatibilidade

- **Versão do jogo:** 1.19.
- **Arquivo vanilla substituído:** `gui/interaction_confirmation.gui`. Conflita com outros mods que substituam esse mesmo arquivo.
- **Tipos derivados:** a linha da lista herda o `widget_character_list_item` que estiver ativo no playset, então mudanças de outros mods nessa linha são preservadas.
- **Marriage Calculation Assistant:** compatível, os dois usam janelas diferentes.
- **Idiomas:** inglês e português do Brasil (`braz_por`).

## Estrutura

```
common/
  character_interactions/tnt_ga_interactions.txt   interação "Procurar guardião (GCA)"
  script_values/tnt_ga_values.txt                   fórmula da nota, projeção e avisos
  scripted_effects/tnt_ga_sort_effects.txt          limpeza do estado da ordenação
  scripted_guis/tnt_ga_sort.txt                     ordenação por nota (portada do MCA)
  scripted_guis/tnt_ga_filter.txt                   filtro de inteligência
  scripted_triggers/tnt_ga_triggers.txt             requisitos de guardião e filtro
gui/
  interaction_confirmation.gui                      vanilla + lista, botões e filtro do GCA (gerado)
  tnt_ga_character_list_item.gui                    linha da lista com a nota (gerado)
localization/
  english/  braz_por/
tools/                                              geradores de GUI e empacotador (package.py)
.github/workflows/release.yml                       zip e Release a cada tag
```

## Desenvolvimento

Os dois arquivos de GUI são gerados por script, porque as expressões são longas e repetidas. Não edite à mão: altere o gerador e rode de novo.

```sh
# 1. Linha da lista (também grava tools/gates.txt, usado no passo 2)
python tools/gen_rows.py tools/row_template.gui gui/tnt_ga_character_list_item.gui tools/gates.txt

# 2. Janela de interação, a partir do arquivo vanilla
python tools/gen_confirm.py tools/gates.txt "<CK3>/game/gui/interaction_confirmation.gui" gui/interaction_confirmation.gui
```

Quando o jogo atualizar, rode o passo 2 com o novo `interaction_confirmation.gui` do vanilla para manter as mudanças da Paradox.

### Lançar uma versão

1. Atualize `version` em `descriptor.mod`.
2. Faça o commit, crie a tag e envie:

   ```sh
   git tag v1.0.1
   git push origin main v1.0.1
   ```

O workflow `.github/workflows/release.yml` gera o zip com `tools/package.py`, confere se a tag bate com a versão do `descriptor.mod` e publica a Release com o zip anexado. Em push e pull request comuns ele só gera o zip como artefato da execução.

Para gerar o zip localmente: `python tools/package.py` (sai em `dist/`).

Para testar, rode o jogo com `-debug_mode` e confira `Documentos/Paradox Interactive/Crusader Kings III/logs/error.log`. O aviso `Event target 'tnt_ga_other' is used but is never set` é esperado: esse scope é preenchido pelo GUI.

---

## English summary

**Guardian Calculation Assistant** shows, for every candidate in the guardian/ward lists, the exact per-birthday chance that the child gains education points with that guardian, plus the projected education rank. It reproduces the vanilla formula (`education_point_acquisition_support_effect`) and reads the vanilla factors, so overhauls that retune them are followed.

It also adds:

- a **Find Guardian (GCA)** interaction that searches your court and every court in diplomatic range, then opens the matching vanilla interaction (Educate Child or Offer Ward) pre-filled;
- **GCA: by score** / **Default list** buttons that sort the search by score (sorted by default);
- a Quick / Intelligent / Genius filter, plus the native trait filter.

It overrides `gui/interaction_confirmation.gui`, targets CK3 1.19 and ships English and Brazilian Portuguese localization.
