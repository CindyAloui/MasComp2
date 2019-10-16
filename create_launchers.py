import io
import os


dir = "data/seeds/seeds-super-supersenses/"
i = 0
launcher_template = io.open("launchForCluster-template.slurm", "r", encoding="utf8")
template = launcher_template.read()
for filename in os.listdir(dir):
    filename = os.path.basename(filename)
    if "seeds." in filename and "not_seeds" not in filename and ".txt" not in filename and "get_" not in filename:
        i+=1
        new_launcher = io.open("launchForCluster-" + str(i) + ".slurm", "w", encoding='utf8')
        new_launcher.write(template.replace("__NAME__", filename + "_train"))
        new_launcher.write("\npython3 train.py data/seeds/seeds-super-supersenses/" + filename + " data/seeds/seeds-super-supersenses/not_" +
                           filename + " data/frWaC/mcf_" + filename + "/ " + filename)
