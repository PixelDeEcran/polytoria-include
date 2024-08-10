from pathlib import Path
from typing import Set, Optional

import typer
import time
import os

app = typer.Typer()

def include(dir: Path, path: Path, including: Set[Path], already_included: Set[Path], is_client: bool) -> Optional[str]:
    including.add(path)

    result = ""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        print("(X) Could not open/read file:", path)
        return None

    skip_line = False
    for line in content.splitlines():
        if not skip_line:
            if line.lstrip().startswith("---#include "):
                other = dir / line[12:]

                if other in including:
                    print("(X) Cyclic dependence detected while including ", other)
                    return None
                
                if not other in already_included:
                    other_result = include(dir, other, including, already_included, is_client)

                    if other_result != None:
                        result = result + other_result + "\n"
                    else:
                        return None
            elif (is_client and line.lstrip().startswith("---#if server then")) or (not is_client and line.lstrip().startswith("---#if client then")):
                skip_line = True
            elif not line.lstrip().startswith("---#if server then") and not line.lstrip().startswith("---#if client then") and not line.lstrip().startswith("---#end"):
                result = result + line + "\n"
        else:
            if line.lstrip().startswith("---#end"):
                skip_line = False

    including.remove(path)
    already_included.add(path)

    return result

class Watcher:
    def __init__(self, source: Path, out: Path):
        self.source = source
        self.out = out
        self.already_included = set()

    def run(self):
        print("* Assemble", self.source, "to", self.out)

        already_included = set()
        content = include(self.source.parent, self.source, set(), already_included, str(self.source).endswith(".client.lua"))

        if content != None:
            self.out.write_text(content, encoding="utf-8")
            self.already_included = already_included
            print(" -> Assembly done!")

        cached_stamps = {}
        for path in self.already_included:
            try:
                cached_stamps[path] = os.stat(path).st_mtime
            except OSError:
                cached_stamps[path] = None

        running = True
        while running:
            time.sleep(1)
            
            for path in self.already_included:
                try:
                    if cached_stamps[path] != os.stat(path).st_mtime:
                        print("Changes detected.")
                        running = False
                        break
                except:
                    if cached_stamps[path] != None:
                        print("Changes detected.")
                        running = False
                        break

        
        self.run()



@app.command()
def main(source: Path, out: Path):
    print("-- POLYTORIA-INCLUDE, by the community, for the community <3! --\n")

    Watcher(source, out).run()


if __name__ == "__main__":
    app()