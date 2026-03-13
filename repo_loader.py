import requests
import zipfile
import io


def load_repo_from_github(repo_url):

    repo_parts = repo_url.replace("https://github.com/", "").split("/")
    owner = repo_parts[0]
    repo = repo_parts[1]

    branches = ["main", "master"]

    response = None

    for branch in branches:
        zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
        response = requests.get(zip_url)

        if response.status_code == 200:
            break

    if response is None or response.status_code != 200:
        raise Exception("Could not download repository zip")

    code_data = []

    extensions = (
        ".py",".js",".ts",".java",".go",".cpp",
        ".lua",".json",".cfg",".txt",".md",".html",".css"
    )

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:

        for file in z.namelist():

            if file.endswith(extensions):

                try:
                    content = z.read(file).decode("utf-8", errors="ignore")

                    code_data.append({
                        "file": file,
                        "content": content
                    })

                except:
                    pass

    return code_data