import cv2
import os

def images_to_video(input_folder, output_file, fps=10):
    # Get the list of image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    image_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

    # Read the first image to get dimensions
    first_image = cv2.imread(os.path.join(input_folder, image_files[0]))
    height, width, _ = first_image.shape

    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use appropriate codec based on your system
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Write each image to the video
    for image_file in image_files:
        img_path = os.path.join(input_folder, image_file)
        frame = cv2.imread(img_path)
        video_writer.write(frame)

    # Release the VideoWriter object
    video_writer.release()

if __name__ == "__main__":
    input_folder = "./4_4_images/small_iter"
    output_file = "4_4_video.mp4"
    fps = 10

    images_to_video(input_folder, output_file, fps)
