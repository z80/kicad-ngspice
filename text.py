import pygtk
pygtk.require('2.0')
import gtk

class TextViewExample:

    def do_manipulations(filename):
        fw = open(filename, 'r')
	    output = open ('netlist_output.cir','w')
    	for line in fw:
    	    cc = re.search("\w\d_\w\d_\w\d",line)
		    newline=line
		if cc:
			nline = re.split("[_]", line)
			newline = ""
			for i in range(0,len(nline)):
				if (i==0):
					newline=newline+nline[i] + "  "
				else :
					if (i==(len(nline)-1)):
						newline=newline+nline[i].replace("  "," ")
					else:
						newline=newline+nline[i]+" "
		else:
			newline = line
			line = line.replace("  "," ").strip()
			correct_cccs=re.split("[_]",line)
			split_line = re.split(" ",line)
			print correct_cccs[0]
			try:
				re.match("^\d",correct_cccs[1])
				value=int(correct_cccs[1])
				var=split_line[5].split("_")
				newline=split_line[0]+"  " + split_line[-3] + " " + split_line[-2]  + " " + var[0]+ " " + var[1]+"\n"
			except:
			#else:
				if (len(split_line)==6):
					if ((split_line[1]=="1")or(split_line[1]=="3")):
						newline=split_line[0] + "  " + "3 " + "4 " + "1 " + "2 " + split_line[5] + "\n"
		if (newline.strip()!= ".end"):
			output.write(newline)
	    output.close()
	    fw.close()
	    ask_for_models=raw_input("Enter models(y/n) ? ").strip()
	    if (ask_for_models=="y"):
		    database_fp=open("database.txt","r")
		    i=1
		    type_model=[""]
		    for line in database_fp:
			    if ((line.strip()!="1>>") and (line.strip()!="")):
				    print str(i) + str(line) 
				    type_model.insert(i-1,str(line.strip()))
				    i+=1
			    else:
				    break
		    model_number = input("Enter model numeber :")
    		selected_model_name=type_model[model_number-1]
	    	model_name = raw_input("Enter model name ").strip()
    		start_line=1
	    	database_fp.close()
		    database_fp=open("database.txt","r")
		    for line in database_fp:
			    if(line.strip()==(str(model_number)+">>")):
				    break
			    else:
				    #print line
				    start_line+=1
        	database_fp.close()
		    model_content=""
    		start_line+=1
	    	print start_line
		    is_read= True
    		while is_read:
	    		line = linecache.getline("database.txt",start_line)
		    	start_line+=1
		    	if (line.strip()==(str(model_number+1)+">>")):
			    	is_read= False
    			else:
	    			model_content = model_content+line.strip()+"\n"
		    model_content=model_content.replace(selected_model_name,model_name)
		    print model_content
    		with open("netlist_output.cir","a") as myfile:
	    		myfile.write(model_content)
		    	myfile.write("\n\n")



	#else:
		#sys.exit(0)
	resp=raw_input("Enter simulation data(y/n)? ")
	if (resp=="y"):
		analysis_type= raw_input("Type of Analysis(AC[a]/Trans[t]): ")
		if (analysis_type=="a"):
			ac_scale=raw_input("Type of Scale : lin/dec/oct: ").strip()
			number_of_data_points=input("Number of Data Points: ")
			start_frequency= raw_input("Enter frequency: ").strip()
			end_frequency = raw_input("Enter end frequency: ").strip()
			appendline_ac_or_trans = ".ac " + str(ac_scale) + " " + str(number_of_data_points)+" " + str(start_frequency) + " " + str(end_frequency) + "\n" 
		elif(analysis_type=="t"):
			print "Enter dat input for Transition analysis"
			start_time = raw_input("Start Time: ").strip()
			end_time = raw_input("End Time: ").strip()
			appendline_ac_or_trans = ".trans" + " " + str(start_time) + " " + str(end_time) + "\n"
		else:
			sys.exit(0)
		appendline_end = ".end\n"
		appendline_control=".control\n" + "run\n" + ".endc\n"
		with open("netlist_output.cir","a") as myfile			myfile.write("\n")
			myfile.write(appendline_ac_or_trans)
			myfile.write("\n\n")
			myfile.write(appendline_end)
			myfile.write("\n\n\n")
			myfile.write(appendline_control)
	else:
		with open("netlist_output.cir","a") as myfile:
			myfile.write("\n.end\n")
    def toggle_editable(self,checkbutton,textview):
        textview.set_editable(checkbutton.get_active())
    def toggle_cursor_visible(self,checkbutton,textview):
        textview.set_editable(checkbutton.get_active())
    def toggle_left_margin(self,checkbutton,textview):
        if checkbutton.get_active():
            textview.set_left_margin(20)
        else:
            textview.set_left_margin(0)
    def toggle_right_margin(self,checkbutton,textview):
        if checkbutton.get_active():
            textview.set_right_margin(20)
        else:
            textview.set_right_margin(0)
    def new_wrap_mode(self, radiobutton, textview, val):
        if radiobutton.get_active():
            textview.set_wrap_mode(val)
    def new_justification(self, radiobutton, textview, val):
        if radiobutton.get_active():
            textview.set_justification(val)
    def close_application(self,widget):
        gtk.main_quit()

    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_resizable(True)
        window.connect("destroy",self.close_application)
        window.set_title("convert ")
        window.set_border_width(10)
        box1=gtk.VBox(False,0)
        window.add(box1)
        box1.show()
        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        sw1 = gtk.ScrolledWindow()
        sw2 = gtk.ScrolledWindow()
        sw1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        sw2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textview1 = gtk.TextView()
        textbuffer1 = textview1.get_buffer()
        textview2 = gtk.TextView()
        textbuffer2 = textview2.get_buffer()
        sw1.add(textview1)
        sw2.add(textview2)
        sw1.show()
        sw2.show()
        textview1.show()
        textview2.show()
        box2.pack_start(sw1)
        box2.pack_start(sw2)
        infile=open("netlist_output.cir","r")
        if infile:
            string = infile.read()
            infile.close()
            textbuffer1.set_text(string)
            textbuffer2.set_text(string)
        hbox = gtk.HButtonBox()
        box2.pack_start(hbox, False, False, 0)
        hbox.show()
        vbox = gtk.VBox()
        vbox.show()
        hbox.pack_start(vbox, False, False, 0)
        check = gtk.CheckButton("Editable")
        vbox.pack_start(check, False, False, 0)
        textview=textview1
        check.connect("toggled", self.toggle_editable, textview)
        check.set_active(True)
        check.show()
        check = gtk.CheckButton("Cursor Visible")
        vbox.pack_start(check, False, False, 0)
        check.connect("toggled", self.toggle_cursor_visible, textview)
        check.set_active(True)
        check.show()
        check = gtk.CheckButton("Left Margin")
        vbox.pack_start(check, False, False, 0)
        check.connect("toggled", self.toggle_left_margin, textview)
        check.set_active(False)
        check.show()
        check = gtk.CheckButton("Right Margin")
        vbox.pack_start(check, False, False, 0)
        check.connect("toggled", self.toggle_right_margin, textview)
        check.set_active(False)
        check.show()
        vbox.show()
        hbox.pack_start(vbox, False, False, 0)
        radio = gtk.RadioButton(None, "WRAP__NONE")
        vbox.pack_start(radio, False, True, 0)
        radio.connect("toggled", self.new_wrap_mode, textview, gtk.WRAP_NONE)
        radio.set_active(True)
        radio.show()
        radio = gtk.RadioButton(radio, "WRAP__CHAR")
        vbox.pack_start(radio, False, True, 0)
        radio.connect("toggled", self.new_wrap_mode, textview, gtk.WRAP_CHAR)
        radio.show()
        radio = gtk.RadioButton(radio, "WRAP__WORD")
        vbox.pack_start(radio, False, True, 0)
        radio.connect("toggled", self.new_wrap_mode, textview, gtk.WRAP_WORD)
        radio.show()
        vbox=gtk.VBox()
        vbox.show()
        hbox.pack_start(radio,False,False,0)
        radio = gtk.RadioButton(None, "JUSTIFY__LEFT")
        vbox.pack_start(radio, False, True, 0)
        radio.connect("toggled", self.new_justification,textview,gtk.JUSTIFY_LEFT)
        radio.set_active(True)
        radio.show()
        radio = gtk.RadioButton(radio, "JUSTIFY__RIGHT")
        vbox.pack_start(radio, False, True, 0)
        radio.connect("toggled", self.new_justification, textview,gtk.JUSTIFY_RIGHT)
        radio.show()
        radio = gtk.RadioButton(radio, "JUSTIFY__CENTER")
        vbox.pack_start(radio, False, True, 0)
        radio.connect("toggled", self.new_justification, textview,gtk.JUSTIFY_CENTER)
        radio.show()
        separator = gtk.HSeparator()
        box1.pack_start(separator, False, True, 0)
        separator.show()
        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, False, True, 0)
        box2.show()
        button = gtk.Button("close")
        button.connect("clicked", self.close_application)
        box2.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()
        window.show()
def main():
    gtk.main()
    return 0
if __name__ == "__main__":
    TextViewExample()
    main()
