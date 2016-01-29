__author__ = 'daniel'


class Pdb():

    def __init__(self):
        self.res = False
        self.fbe_min = []
        self.fbe_max = []

    def iopdb(self, key, save_dir, rmsd):
        self.fbe_list = []
        self.fbe_listL = []
        try:
            file = open(key, "r")
            wrt = file.name
            wrt = wrt.replace("dlg", "pdb")
        except:
            print "Error"

        try:
            doc = open(save_dir + "/" + wrt, "w")

        except:
            doc = open(wrt, "w")
            tkMessageBox.showinfo("Advertencia", "El trabajo se guardara en " + str(os.getcwd()))

        searchstrings = ("DOCKED: MODEL", "DOCKED: ATOM",
                         "DOCKED: USER    Estimated Free Energy of Binding", "DOCKED: TER")
        list_of_list = []
        temp_list = []

        for line in file.readlines():
            if "BEGIN_RES" in line.split():
                self.res = True
            if "END_RES" in line.split():
                self.res = False
            for word in searchstrings:
                if word in line:
                    incoming_data = []
                    if word == "DOCKED: MODEL":
                        incoming_data.extend(line.split())
                        temp_list.append(incoming_data[2])
                        line2 = line.replace("DOCKED: ", "")
                        doc.writelines(line2)
                        del incoming_data[:]
                    elif word == "DOCKED: USER    Estimated Free Energy of Binding":
                        incoming_data.extend(line.split())
                        temp_list.append(incoming_data[-3])
                        self.fbe_list.append(float(incoming_data[-3]))
                        line2 = line.replace("DOCKED: ", "")
                        doc.writelines(line2)
                        del incoming_data[:]
                    elif word == "DOCKED: ATOM":
                        if self.res is False:
                            incoming_data.extend(line.split())
                            del incoming_data[:1]
                            temp_list.append(" ".join(incoming_data))
                            del incoming_data[:]
                        line2 = line.replace("DOCKED: ", "")
                        lne = line2.replace("A", "C")
                        lne = lne.replace("CTOM", "ATOM")
                        doc.writelines(lne)
                    elif word == "DOCKED: TER":
                        incoming_data.extend(line.split())
                        del incoming_data[0]
                        temp_list.append(incoming_data[0])
                        del incoming_data[:]
                        list_of_list.append(temp_list[:])
                        del temp_list[:]
                        line2 = line.replace("DOCKED: ", "")
                        doc.writelines(line2)
                        doc.writelines("ENDMDL\n")
        self.fbe_listL.extend(self.fbe_list)
        doc.close()
        return list_of_list, self.fbe_listL

    def lst_num(self, dosd_list):
        temp_elist = []
        scn_tmp_list = []
        scn_list_list = []
        self.list_elem = len(dosd_list)
        for con in range(0, self.list_elem):
            for elem in dosd_list[con]:
                thiss = elem.split()
                if 1 < len(thiss) < 13:
                    temp_elist.extend(thiss[5:8])
                elif len(thiss) == 13:
                    temp_elist.extend(thiss[6:9])
            temp_elist = [float(i) for i in temp_elist]
            scn_list_list.append(temp_elist[:])
            del temp_elist[:]
        del scn_tmp_list[:]
        #print scn_list_list
        return scn_list_list
