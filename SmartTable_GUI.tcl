#############################################################################
# Generated by PAGE version 4.13
# in conjunction with Tcl version 8.6
set vTcl(timestamp) ""


if {!$vTcl(borrow)} {

set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #d9d9d9
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #d8d8d8
set vTcl(active_menu_fg) #000000
}

#################################
#LIBRARY PROCEDURES
#


if {[info exists vTcl(sourcing)]} {

proc vTcl:project:info {} {
    set base .top37
    global vTcl
    set base $vTcl(btop)
    if {$base == ""} {
        set base .top37
    }
    namespace eval ::widgets::$base {
        set dflt,origin 0
        set runvisible 1
    }
    set site_3_0 $base.fra38
    set site_3_0 $base.fra56
    namespace eval ::widgets_bindings {
        set tagslist _TopLevel
    }
    namespace eval ::vTcl::modules::main {
        set procs {
        }
        set compounds {
        }
        set projectType single
    }
}
}

#################################
# GENERATED GUI PROCEDURES
#

proc vTclWindow.top37 {base} {
    if {$base == ""} {
        set base .top37
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background {#d9d9d9} -highlightbackground {#d9d9d9} \
        -highlightcolor black 
    wm focusmodel $top passive
    wm geometry $top 377x379+417+148
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 1354 733
    wm minsize $top 120 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    wm title $top "Smart Table"
    vTcl:DefineAlias "$top" "Toplevel1" vTcl:Toplevel:WidgetProc "" 1
    frame $top.fra38 \
        -borderwidth 2 -relief groove -background {#d9d9d9} -height 265 \
        -highlightbackground {#d9d9d9} -highlightcolor black -width 355 
    vTcl:DefineAlias "$top.fra38" "frameData" vTcl:WidgetProc "Toplevel1" 1
    set site_3_0 $top.fra38
    label $site_3_0.lab39 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -text {Style No.} 
    vTcl:DefineAlias "$site_3_0.lab39" "lblStyleNo" vTcl:WidgetProc "Toplevel1" 1
    label $site_3_0.lab40 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -text Size 
    vTcl:DefineAlias "$site_3_0.lab40" "lblSize" vTcl:WidgetProc "Toplevel1" 1
    label $site_3_0.lab41 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -text {Body Height} 
    vTcl:DefineAlias "$site_3_0.lab41" "lblBodyHeight" vTcl:WidgetProc "Toplevel1" 1
    label $site_3_0.lab42 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -text {Body Width} 
    vTcl:DefineAlias "$site_3_0.lab42" "lblBodyWidth" vTcl:WidgetProc "Toplevel1" 1
    label $site_3_0.lab43 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -text {Body Sweap} 
    vTcl:DefineAlias "$site_3_0.lab43" "lblBodySweap" vTcl:WidgetProc "Toplevel1" 1
    label $site_3_0.lab44 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -text {Back Neck Width} 
    vTcl:DefineAlias "$site_3_0.lab44" "lblBackNeckWidth" vTcl:WidgetProc "Toplevel1" 1
    entry $site_3_0.ent50 \
        -background white -disabledforeground {#a3a3a3} -font TkFixedFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -insertbackground black \
        -selectbackground {#c4c4c4} -selectforeground black 
    vTcl:DefineAlias "$site_3_0.ent50" "txtStyleNo" vTcl:WidgetProc "Toplevel1" 1
    entry $site_3_0.ent51 \
        -background white -disabledforeground {#a3a3a3} -font TkFixedFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -insertbackground black \
        -selectbackground {#c4c4c4} -selectforeground black 
    vTcl:DefineAlias "$site_3_0.ent51" "txtSize" vTcl:WidgetProc "Toplevel1" 1
    entry $site_3_0.ent52 \
        -background white -disabledforeground {#a3a3a3} -font TkFixedFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -insertbackground black \
        -selectbackground {#c4c4c4} -selectforeground black 
    vTcl:DefineAlias "$site_3_0.ent52" "txtBodyHeight" vTcl:WidgetProc "Toplevel1" 1
    entry $site_3_0.ent53 \
        -background white -disabledforeground {#a3a3a3} -font TkFixedFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -insertbackground black \
        -selectbackground {#c4c4c4} -selectforeground black 
    vTcl:DefineAlias "$site_3_0.ent53" "txtBodyWidth" vTcl:WidgetProc "Toplevel1" 1
    entry $site_3_0.ent54 \
        -background white -disabledforeground {#a3a3a3} -font TkFixedFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -insertbackground black \
        -selectbackground {#c4c4c4} -selectforeground black 
    vTcl:DefineAlias "$site_3_0.ent54" "txtBodySweap" vTcl:WidgetProc "Toplevel1" 1
    entry $site_3_0.ent55 \
        -background white -disabledforeground {#a3a3a3} -font TkFixedFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -insertbackground black \
        -selectbackground {#c4c4c4} -selectforeground black 
    vTcl:DefineAlias "$site_3_0.ent55" "txtBackNeckWidth" vTcl:WidgetProc "Toplevel1" 1
    place $site_3_0.lab39 \
        -in $site_3_0 -x 20 -y 20 -anchor nw -bordermode ignore 
    place $site_3_0.lab40 \
        -in $site_3_0 -x 20 -y 60 -anchor nw -bordermode ignore 
    place $site_3_0.lab41 \
        -in $site_3_0 -x 15 -y 100 -width 84 -relwidth 0 -height 21 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.lab42 \
        -in $site_3_0 -x 20 -y 140 -anchor nw -bordermode ignore 
    place $site_3_0.lab43 \
        -in $site_3_0 -x 20 -y 180 -anchor nw -bordermode ignore 
    place $site_3_0.lab44 \
        -in $site_3_0 -x 20 -y 220 -anchor nw -bordermode ignore 
    place $site_3_0.ent50 \
        -in $site_3_0 -x 170 -y 20 -anchor nw -bordermode ignore 
    place $site_3_0.ent51 \
        -in $site_3_0 -x 170 -y 60 -anchor nw -bordermode ignore 
    place $site_3_0.ent52 \
        -in $site_3_0 -x 170 -y 100 -width 164 -height 20 -anchor nw \
        -bordermode ignore 
    place $site_3_0.ent53 \
        -in $site_3_0 -x 170 -y 140 -width 164 -height 20 -anchor nw \
        -bordermode ignore 
    place $site_3_0.ent54 \
        -in $site_3_0 -x 170 -y 180 -anchor nw -bordermode ignore 
    place $site_3_0.ent55 \
        -in $site_3_0 -x 170 -y 220 -anchor nw -bordermode ignore 
    frame $top.fra56 \
        -borderwidth 2 -relief groove -background {#d9d9d9} -height 75 \
        -highlightbackground {#d9d9d9} -highlightcolor black -width 355 
    vTcl:DefineAlias "$top.fra56" "frameRun" vTcl:WidgetProc "Toplevel1" 1
    set site_3_0 $top.fra56
    button $site_3_0.but57 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -foreground {#000000} -highlightbackground {#000000} \
        -highlightcolor {#000000} -pady 0 -state active -text Run 
    vTcl:DefineAlias "$site_3_0.but57" "btnRun" vTcl:WidgetProc "Toplevel1" 1
    button $site_3_0.but58 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -state active -text Stop 
    vTcl:DefineAlias "$site_3_0.but58" "btnStop" vTcl:WidgetProc "Toplevel1" 1
    place $site_3_0.but57 \
        -in $site_3_0 -x 70 -y 10 -width 62 -relwidth 0 -height 54 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but58 \
        -in $site_3_0 -x 210 -y 10 -width 65 -relwidth 0 -height 54 \
        -relheight 0 -anchor nw -bordermode ignore 
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.fra38 \
        -in $top -x 10 -y 10 -width 355 -relwidth 0 -height 265 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.fra56 \
        -in $top -x 10 -y 290 -width 355 -relwidth 0 -height 75 -relheight 0 \
        -anchor nw -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

#############################################################################
## Binding tag:  _TopLevel

bind "_TopLevel" <<Create>> {
    if {![info exists _topcount]} {set _topcount 0}; incr _topcount
}
bind "_TopLevel" <<DeleteWindow>> {
    if {[set ::%W::_modal]} {
                vTcl:Toplevel:WidgetProc %W endmodal
            } else {
                destroy %W; if {$_topcount == 0} {exit}
            }
}
bind "_TopLevel" <Destroy> {
    if {[winfo toplevel %W] == "%W"} {incr _topcount -1}
}

set btop ""
if {$vTcl(borrow)} {
    set btop .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop $vTcl(tops)] != -1} {
        set btop .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop
Window show .
Window show .top37 $btop
if {$vTcl(borrow)} {
    $btop configure -background plum
}

