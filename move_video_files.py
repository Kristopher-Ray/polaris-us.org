import os
import shutil
import yaml

def create_media_dir():
    """Create the media directory if it doesn't exist."""
    media_dir = os.path.join('content', 'media')
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    return media_dir

def has_videos_category(file_path):
    """Check if a file has the Videos category."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Read until we find the YAML front matter
            content = ""
            in_frontmatter = False
            frontmatter_count = 0
            
            for line in f:
                if line.strip() == '---':
                    frontmatter_count += 1
                    in_frontmatter = True
                    if frontmatter_count == 2:
                        break
                if in_frontmatter and frontmatter_count == 1:
                    content += line
            
            # Parse the YAML front matter
            if content:
                metadata = yaml.safe_load(content)
                if metadata and 'categories' in metadata:
                    return 'Videos' in metadata['categories']
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
    return False

def move_video_files():
    """Move all files with Videos category to media directory."""
    updates_dir = os.path.join('content', 'updates')
    media_dir = create_media_dir()
    moved_files = []
    
    # Ensure updates directory exists
    if not os.path.exists(updates_dir):
        print(f"Updates directory not found at {updates_dir}")
        return
    
    # Process each file in updates directory
    for filename in os.listdir(updates_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(updates_dir, filename)
            if has_videos_category(file_path):
                try:
                    # Move the file
                    shutil.move(file_path, os.path.join(media_dir, filename))
                    moved_files.append(filename)
                except Exception as e:
                    print(f"Error moving {filename}: {str(e)}")
    
    # Print summary
    print(f"\nMoved {len(moved_files)} files to {media_dir}")
    print("\nMoved files:")
    for file in moved_files:
        print(f"- {file}")

if __name__ == "__main__":
    move_video_files()