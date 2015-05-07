            





            so = open("namefil", "r+")
            for cell in cells:
                # name cell
                sa = str(get_name(cell))
                da = str(get_dBm(cell))
                ga = str(get_address(cell))
                so.write(sa)
                so.write(" ")
                so.write(da)
                so.write(" ")
                so.write(ga)
                so.write("\n")
            so.close()