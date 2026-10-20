# Generates gui/interaction_confirmation.gui from the vanilla file.
# Usage: python tools/gen_confirm.py tools/gates.txt <CK3>/game/gui/interaction_confirmation.gui gui/interaction_confirmation.gui
import sys
vg, gg = open(sys.argv[1], encoding='utf-8').read().strip().split('\n')
src, dst = sys.argv[2], sys.argv[3]
GATE = f"Or( {vg}, {gg} )"
t = open(src, encoding='utf-8-sig').read().replace('\r\n', '\n')

W = "CharacterInteractionConfirmationWindow"
VS = "GetVariableSystem"
SIZE = "GetDataModelSize( CharacterSelectionList.GetList )"

# ---- intellect filter -------------------------------------------------
VAR = lambda n: f"GetPlayer.MakeScope.GetVariable('tnt_ga_f{n}').IsSet"
ANY = f"Or( Or( {VAR(1)}, {VAR(2)} ), {VAR(3)} )"
LVL = "GuiScope.SetRoot( CharacterListItem.GetCharacter.MakeScope ).ScriptValue('tnt_ga_intellect_level_value')"
MATCH = (f"Or( Or( And( {VAR(1)}, EqualTo_CFixedPoint( {LVL}, '(CFixedPoint)1' ) ), "
         f"And( {VAR(2)}, EqualTo_CFixedPoint( {LVL}, '(CFixedPoint)2' ) ) ), "
         f"And( {VAR(3)}, EqualTo_CFixedPoint( {LVL}, '(CFixedPoint)3' ) ) )")

# ---- sort context -----------------------------------------------------
STATE = "GetPlayer.MakeScope.GetVariable('tnt_ga_sort_state').GetValueWithDefault('(CFixedPoint)0')"
ST = lambda n: f"EqualTo_CFixedPoint( {STATE}, '(CFixedPoint){n}' )"
ST_ACTIVE = f"GreaterThan_CFixedPoint( {STATE}, '(CFixedPoint)0' )"
CTX = (f".AddScope('tnt_ga_sort_n', MakeScopeValue( IntToFixedPoint( {SIZE} ) ))"
       f".AddScope('tnt_ga_sort_ward', {W}.GetRecipient.MakeScope)"
       f".AddScope('tnt_ga_sort_day', MakeScopeValue( IntToFixedPoint( GetCurrentDate.GetDateAsTotalDays ) ))")
VALID = f"GetScriptedGui('tnt_ga_sort_context_valid').IsValid( GuiScope.SetRoot( GetPlayer.MakeScope ){CTX}.End )"
START = f"GetScriptedGui('tnt_ga_sort_start').Execute( GuiScope.SetRoot( GetPlayer.MakeScope ){CTX}.End )"
CLEAR = "GetScriptedGui('tnt_ga_sort_clear').Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )"
COLLECT = (f"GetScriptedGui('tnt_ga_sort_collect').Execute( GuiScope.SetRoot( CharacterListItem.GetCharacter.MakeScope )"
           f".AddScope('actor', GetPlayer.MakeScope).AddScope('tnt_ga_other', {W}.GetRecipient.MakeScope){CTX}"
           f".AddScope('tnt_ga_sort_index', MakeScopeValue( IntToFixedPoint( PdxGuiWidget.GetIndexInDataModel ) )).End )")
SIZE_OK = f"And( GreaterThan_int32( {SIZE}, '(int32)0' ), LessThanOrEqualTo_int32( {SIZE}, '(int32)99999' ) )"
CAN_START = f"And( Not( {ST_ACTIVE} ), And( Not( CharacterSelectionList.IsBuildingList ), And( Not( CharacterSelectionList.FiltersShown ), {SIZE_OK} ) ) )"
AUTO = f"And( {gg}, And( Not( {VS}.Exists( 'tnt_ga_sort_auto' ) ), {CAN_START} ) )"
INVALIDATE = f"And( {ST_ACTIVE}, Or( CharacterSelectionList.IsBuildingList, Not( {VALID} ) ) )"
COMPLETE = (f"And( {ST(1)}, And( Not( CharacterSelectionList.IsBuildingList ), And( EqualTo_CFixedPoint( "
            f"GetPlayer.MakeScope.GetVariable('tnt_ga_sort_received').GetValueWithDefault('(CFixedPoint)0'), "
            f"GetPlayer.MakeScope.GetVariable('tnt_ga_sort_expected').GetValueWithDefault('(CFixedPoint)0') ), {VALID} ) ) )")
DIR = "GetPlayer.MakeScope.GetVariable('tnt_ga_sort_direction').GetValueWithDefault('(CFixedPoint)0')"
DECODED = "Subtract_CFixedPoint( Divide_CFixedPoint( Subtract_CFixedPoint( Scope.GetValue, Modulo_CFixedPoint( Scope.GetValue, '(CFixedPoint)100000' ) ), '(CFixedPoint)100000' ), '(CFixedPoint)10000' )"
FRESH = f"GuiScope.SetRoot( CharacterListItem.GetCharacter.MakeScope ).AddScope('tnt_ga_other', {W}.GetRecipient.MakeScope).ScriptValue('tnt_ga_sort_capture_value')"
SCORE_GUARD = f"EqualTo_CFixedPoint( {FRESH}, {DECODED} )"
NATIVE_IDX = "Subtract_CFixedPoint( '(CFixedPoint)99999', Modulo_CFixedPoint( Scope.GetValue, '(CFixedPoint)100000' ) )"
CAND_IDX = (f"FixedPointToInt( Select_CFixedPoint( EqualTo_CFixedPoint( {DIR}, '(CFixedPoint)1' ), {NATIVE_IDX}, "
            f"Subtract_CFixedPoint( Subtract_CFixedPoint( GetPlayer.MakeScope.GetVariable('tnt_ga_sort_expected').GetValueWithDefault('(CFixedPoint)0'), '(CFixedPoint)1' ), {NATIVE_IDX} ) ) )")
ID_GUARD = (f"And( Or( EqualTo_CFixedPoint( {DIR}, '(CFixedPoint)1' ), EqualTo_CFixedPoint( {DIR}, '(CFixedPoint)-1' ) ), "
            f"ObjectsEqual( CharacterListItem.GetCharacter, Scope.Char ) )")


def cb(n, key):
    exe = (f"GetScriptedGui('tnt_ga_toggle_filter').Execute( GuiScope.SetRoot( GetPlayer.MakeScope )"
           f".AddScope( 'tnt_ga_level', MakeScopeValue( '(CFixedPoint){n}' ) )"
           f".AddScope( 'tnt_ga_reopen', MakeScopeValue( Select_CFixedPoint( {gg}, '(CFixedPoint)1', '(CFixedPoint)0' ) ) )"
           f".AddScope( 'tnt_ga_ward', {W}.GetRecipient.MakeScope ).End )")
    return f'''				button_checkbox_label = {{
					onclick = "[{VS}.Clear( 'tnt_ga_sort_auto' )]"
					onclick = "[{exe}]"
					tooltip = "tnt_ga_filter_tt"
					blockoverride "checkbox" {{
						checked = "[{VAR(n)}]"
					}}
					blockoverride "text" {{
						text = "{key}"
					}}
				}}
'''


bar = f'''			# GCA: intellect filter for guardian/ward lists. No box ticked = everyone.
			# GCA search: applied by populate_recipient_list (window reopens).
			# Vanilla guardian interactions: rows are hidden in the GUI.
			hbox = {{
				name = "tnt_ga_intellect_filter"
				visible = "[And( {GATE}, Not( {W}.HasPickedCharacters ) )]"
				layoutpolicy_horizontal = expanding
				margin = {{ 20 4 }}
				spacing = 15

				text_single = {{
					text = "tnt_ga_filter_label"
					align = nobaseline
					default_format = "#low"
				}}
{cb(1, 'tnt_ga_filter_quick')}{cb(2, 'tnt_ga_filter_intelligent')}{cb(3, 'tnt_ga_filter_genius')}
				expand = {{}}
			}}

			vbox_interaction_character_list = {{'''
old = "\t\t\tvbox_interaction_character_list = {"
assert t.count(old) == 1
t = t.replace(old, bar, 1)

old2 = '''				blockoverride "item_size"
				{
					size = { 600 110 }
					layoutpolicy_horizontal = expanding

				}
'''
new2 = old2 + f'''
				# GCA score sort (ported from MCA): saveable player snapshot, cleared
				# when the list closes. Callback states need a valid property.
				state = {{
					name = _hide
					scale = 1
					on_start = "[{VS}.Clear( 'tnt_ga_sort_auto' )]"
					on_start = "[{CLEAR}]"
				}}

				# Native sort dropdown kept; GCA buttons below it, GCA search only.
				blockoverride "sort_buttons" {{
					vbox = {{
						layoutpolicy_horizontal = expanding
						spacing = 4
						hbox_list_sort_buttons = {{
							layoutpolicy_horizontal = expanding
							enabled = "[Not( {ST_ACTIVE} )]"
							blockoverride "margins" {{
								margin_left = 20
								margin_right = 23
								margin_top = 5
								spacing = 5
							}}
						}}
						hbox = {{
							visible = "[{gg}]"
							margin_left = 20
							margin_right = 23
							spacing = 8
							button_standard = {{
								name = "tnt_ga_sort_start_button"
								tooltip = "[SelectLocalization( GreaterThan_int32( {SIZE}, '(int32)99999' ), 'tnt_ga_sort_too_many', 'tnt_ga_sort_help' )]"
								size = {{ 180 30 }}
								enabled = "[{CAN_START}]"
								onclick = "[{START}]"
								text_single = {{
									parentanchor = center
									text = "tnt_ga_sort_score_button"
									alwaystransparent = yes
								}}
							}}
							button_standard = {{
								name = "tnt_ga_sort_native_button"
								tooltip = "tnt_ga_sort_help"
								size = {{ 160 30 }}
								enabled = "[{ST_ACTIVE}]"
								onclick = "[{VS}.Set( 'tnt_ga_sort_auto', 'yes' )]"
								onclick = "[{CLEAR}]"
								text_single = {{
									parentanchor = center
									text = "tnt_ga_sort_native_button"
									alwaystransparent = yes
								}}
							}}
							text_single = {{
								name = "tnt_ga_sort_progress"
								layoutpolicy_horizontal = expanding
								align = nobaseline
								visible = "[{ST_ACTIVE}]"
								text = "[SelectLocalization( {ST(1)}, 'tnt_ga_sort_collecting', Select_CString( {ST(2)}, 'tnt_ga_sort_active', 'tnt_ga_sort_failed' ) )]"
								alwaystransparent = yes
							}}
						}}
					}}
				}}

				# Full-list collector keeps GetIndexInDataModel on the actual item widget.
				widget = {{
					name = "tnt_ga_sort_collector"
					size = {{ 1 1 }}
					alwaystransparent = yes
					visible = "[And( {gg}, Not( CharacterSelectionList.IsBuildingList ) )]"
					datamodel = "[DataModelSubSpan( CharacterSelectionList.GetList, '(int32)0', Select_int32( {gg}, {SIZE}, '(int32)0' ) )]"
					datamodel_reuse_widgets = yes
					item = {{
						widget = {{
							name = "tnt_ga_sort_capture"
							size = {{ 1 1 }}
							alwaystransparent = yes
							state = {{
								name = "tnt_ga_sort_capture_active"
								scale = 1
								trigger_when = "[And( {ST(1)}, Not( CharacterSelectionList.IsBuildingList ) )]"
								on_start = "[{COLLECT}]"
							}}
							state = {{
								name = "tnt_ga_sort_capture_idle"
								scale = 1
								trigger_when = "[Not( And( {ST(1)}, Not( CharacterSelectionList.IsBuildingList ) ) )]"
							}}
						}}
					}}
				}}

				# Auto-start once per opening (default = best GCA first), invalidate on
				# any context change, finalize when every row has reported.
				widget = {{
					name = "tnt_ga_sort_controller"
					size = {{ 1 1 }}
					alwaystransparent = yes
					state = {{
						name = "tnt_ga_sort_autostart"
						scale = 1
						trigger_when = "[{AUTO}]"
						on_start = "[{VS}.Set( 'tnt_ga_sort_auto', 'yes' )]"
						on_start = "[{START}]"
					}}
					state = {{
						name = "tnt_ga_sort_invalidate"
						scale = 1
						trigger_when = "[{INVALIDATE}]"
						on_start = "[{CLEAR}]"
					}}
					state = {{
						name = "tnt_ga_sort_complete"
						scale = 1
						trigger_when = "[{COMPLETE}]"
						on_start = "[GetScriptedGui('tnt_ga_sort_finalize').Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
					}}
					state = {{
						name = "tnt_ga_sort_controller_idle"
						scale = 1
						trigger_when = "[Not( Or( Or( {AUTO}, {INVALIDATE} ), {COMPLETE} ) )]"
					}}
				}}

				# GCA: the GCA search can list thousands of characters, so it uses a
				# virtualized grid like the vanilla marriage window. Every other
				# interaction keeps the vanilla vbox, with GUI-side intellect filtering.
				# Each container gets an empty span when it is not the active one.
				blockoverride "container_implementation"
				{{
					vbox = {{
						name = "characters_grid"
						datamodel = "[DataModelSubSpan( CharacterSelectionList.GetList, '(int32)0', Select_int32( {gg}, '(int32)0', {SIZE} ) )]"
						visible = "[And( Not( CharacterSelectionList.IsBuildingList ), Not( {gg} ) )]"
						layoutpolicy_horizontal = expanding
						ignoreinvisible = yes

						item = {{
							tnt_ga_widget_character_list_item = {{
								visible = "[Or( Not( {GATE} ), Or( Not( {ANY} ), {MATCH} ) )]"
								size = {{ 600 110 }}
								layoutpolicy_horizontal = expanding
							}}
						}}
					}}

					fixedgridbox = {{
						name = "tnt_ga_characters_grid"
						datamodel = "[DataModelSubSpan( CharacterSelectionList.GetList, '(int32)0', Select_int32( {gg}, {SIZE}, '(int32)0' ) )]"
						visible = "[And( And( Not( CharacterSelectionList.IsBuildingList ), {gg} ), Not( {ST(2)} ) )]"
						datamodel_reuse_widgets = yes
						addcolumn = 600
						addrow = 110

						item = {{
							tnt_ga_widget_character_list_item = {{
								size = {{ 600 110 }}
							}}
						}}
					}}

					# Native index -> native item -> score packet -> captured reference.
					# Rows show only while their fresh score and identity still match.
					fixedgridbox = {{
						name = "tnt_ga_sorted_characters_grid"
						visible = "[And( And( {ST(2)}, Not( CharacterSelectionList.IsBuildingList ) ), {gg} )]"
						enabled = "[And( Not( CharacterSelectionList.IsBuildingList ), {VALID} )]"
						datamodel = "[GetPlayer.MakeScope.GetList('tnt_ga_sort_indices')]"
						datamodel_reuse_widgets = yes
						addcolumn = 600
						addrow = 110
						item = {{
							widget = {{
								size = {{ 600 110 }}
								datamodel = "[DataModelSubSpan( CharacterSelectionList.GetList, FixedPointToInt( Scope.GetValue ), '(int32)1' )]"
								item = {{
									widget = {{
										size = {{ 600 110 }}
										datamodel = "[DataModelSubSpan( GetPlayer.MakeScope.GetList('tnt_ga_sort_keys_by_index'), FixedPointToInt( Scope.GetValue ), '(int32)1' )]"
										item = {{
											widget = {{
												size = {{ 600 110 }}
												name = "tnt_ga_sort_row_score_guard"
												visible = "[{SCORE_GUARD}]"
												enabled = "[{SCORE_GUARD}]"
												widget = {{
													size = {{ 600 110 }}
													datamodel = "[DataModelSubSpan( GetPlayer.MakeScope.GetList('tnt_ga_sort_candidates'), {CAND_IDX}, '(int32)1' )]"
													item = {{
														widget = {{
															size = {{ 600 110 }}
															name = "tnt_ga_sort_row_identity_guard"
															visible = "[{ID_GUARD}]"
															enabled = "[{ID_GUARD}]"
															tnt_ga_widget_character_list_item = {{
																size = {{ 600 110 }}
															}}
														}}
													}}
												}}
											}}
										}}
									}}
								}}
							}}
						}}
					}}
				}}
'''
assert t.count(old2) == 1, 'old2'
t = t.replace(old2, new2, 1)

old3 = """				datacontext = "[CharacterSelectionList.GetFilter('dynasty_filter')]"
			}"""
assert t.count(old3) == 1, 'old3'
t = t.replace(old3, old3 + "\n\n\t\t\t# GCA: native trait filter, as in the marriage window.\n\t\t\tfilter_item = {\n\t\t\t\tlayoutpolicy_horizontal = expanding\n\t\t\t\tdatacontext = \"[CharacterSelectionList.GetFilter('trait_filter')]\"\n\t\t\t}", 1)
open(dst, 'w', encoding='utf-8-sig', newline='').write(t.replace('\n', '\r\n'))
print('ok')
