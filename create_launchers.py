import io
import os


dir = "data/seeds/seeds-super-supersenses/"
i = 0
launcher_template = io.open("launchForCluster-template.slurm", "r", encoding="utf8")
template = launcher_template.read()
# for filename in os.listdir("data/frWaC/10000-nouns-mcf"):
for filename in os.listdir(dir):
    base_filename = os.path.basename(filename)
    if "seeds." in filename and "not_seeds" not in filename and ".txt" not in filename and ".py" not in filename:
        i+=1
# for i in range(10):
        new_launcher = io.open("train_launchers/launchForCluster-" + base_filename + ".slurm", "w", encoding='utf8')
        new_launcher.write(template.replace("__NAME__", "out/train_" + base_filename))
        new_launcher.write("\npython3 train.py data/seeds/seeds-super-supersenses/" + base_filename + " data/seeds/seeds-super-supersenses/not_" +
                               base_filename + " data/frWaC/mcf_" + base_filename + "/ " + base_filename)
    # new_launcher.write("\ntime python3 compute_context_scores.py data/frWaC/10000-nouns.txt " + filename)

for filename in os.listdir("data/frWaC/10000-nouns-mcf"):
    base_filename = os.path.basename(filename[:-4])
    new_launcher = io.open("contexts_launchers/launchForCluster-" + base_filename + ".slurm", "w", encoding='utf8')
    new_launcher.write(template.replace("__NAME__", "out/context_" + base_filename))
    new_launcher.write("\ntime python3 compute_context_scores.py data/nouns_lists/10000-nouns.txt " + filename)
