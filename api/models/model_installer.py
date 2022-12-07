import os
import shutil

try:
    import nudenet
except ImportError:
    print("NudeNet not installed. Please install nudeNet using the following command: pip install --upgrade nudenet")

home = os.path.expanduser("~")
model_folder = os.path.join(home, ".NudeNet/")

if not os.path.exists(model_folder):
    os.makedirs(model_folder)

# Replace or copy the model files to the model folder
model_files = ["classifier_model.onnx", "classifier_lite.onnx"]
for model_file in model_files:
    model_path = os.path.join(model_folder, model_file)
    # Replace the model file if it already exists
    if os.path.exists(model_path):
        os.remove(model_path)
    # Copy the model file
    print("Copying ./{} to {}".format(model_file, model_path))
    shutil.copy(f"./api/models/{model_file}", model_folder)

print("Model files copied to {}".format(model_folder))


