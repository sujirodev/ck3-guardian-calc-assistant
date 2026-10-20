# Generates gui/tnt_ga_character_list_item.gui from tools/row_template.gui.
# Usage: python tools/gen_rows.py tools/row_template.gui gui/tnt_ga_character_list_item.gui tools/gates.txt
import sys
tpl=open(sys.argv[1],encoding='utf-8').read()
W="CharacterInteractionConfirmationWindow"
vanilla_gate=(f"Or( Or( EqualTo_string( {W}.GetActorSecondaryLabel, Localize('actor_secondary_educate_child_interaction') ), "
      f"EqualTo_string( {W}.GetActorSecondaryLabel, Localize('actor_secondary_offer_guardianship_interaction') ) ), "
      f"EqualTo_string( {W}.GetRecipientSecondaryLabel, Localize('recipient_secondary_offer_ward_interaction') ) )")
gca_gate=f"EqualTo_string( {W}.GetRecipientSecondaryLabel, Localize('recipient_secondary_tnt_ga_find_guardian_interaction') )"
def v(side,pick,other,gate,comment):
    s=f"GuiScope.SetRoot( Character.MakeScope ).AddScope( 'tnt_ga_other', {W}.{other}.MakeScope )"
    return tpl.replace('@S@',s).replace('@PICK@',f"{W}.{pick}").replace('@GATE@',gate).replace('@SIDE@',side).replace('@COMMENT@',comment)
body="\n".join([
 v('a','IsPickingSecondaryActor','GetSecondaryRecipient',vanilla_gate,'Vanilla, picking the secondary actor: the other pair member is the secondary recipient.'),
 v('b','IsPickingSecondaryRecipient','GetSecondaryActor',vanilla_gate,'Vanilla, picking the secondary recipient: the other pair member is the secondary actor.'),
 v('c','IsPickingSecondaryRecipient','GetRecipient',gca_gate,'GCA search: the row is a guardian candidate, the recipient is the ward.'),
])
out=f'''\ufeff########################################################################
# Guardian Calculation Assistant 1.0
#
# Derived row for the generic interaction list. The vanilla/TC
# widget_character_list_item stays untouched; this type inherits whatever
# the playset supplies and only fills its character_relation block.
# Scores show only in Educate Child, Offer Guardianship, Offer Ward and
# the GCA guardian search, identified by their secondary-character
# labels, and only when the other slot holds the matching adult/child.
########################################################################

types TntGuardianAssistant
{{
	type tnt_ga_widget_character_list_item = widget_character_list_item {{
		blockoverride "character_relation" {{
			hbox = {{
				name = "tnt_ga_grade_and_relation"
				ignoreinvisible = yes
				layoutpolicy_horizontal = expanding
				min_height = 26
				spacing = 6

{body}
				text_single = {{
					name = "character_relation"
					layoutpolicy_horizontal = expanding
					raw_text = "|  [Character.GetRelationToString( GetPlayer )]"
					tooltip = "EXTENDED_RELATIONS_TOOLTIP"
					default_format = "#low"
					autoresize = no
					align = nobaseline
					visible = "[Character.HasRelationTo( GetPlayer )]"
					alwaystransparent = yes
				}}

				expand = {{
					visible = "[Not(Character.HasRelationTo( GetPlayer ))]"
				}}
			}}
		}}
	}}
}}
'''
open(sys.argv[2],'w',encoding='utf-8',newline='\n').write(out)
# Gates for tools/gen_confirm.py, one per line.
open(sys.argv[3],'w',encoding='utf-8').write(vanilla_gate + "\n" + gca_gate + "\n")
