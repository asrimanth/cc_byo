use std::env;
use std::fs;
use std::io::{self, BufReader, BufRead};

#[derive(Debug)]
struct WcOptions {
    count_lines: bool,
    count_words: bool,
    count_bytes: bool,
    count_chars: bool,
}

impl WcOptions {
    fn new() -> Self {
        WcOptions {
            count_lines: false,
            count_words: false,
            count_bytes: false,
            count_chars: false,
        }
    }
}

#[derive(Debug, PartialEq)]
struct WcCounts {
    num_lines: usize,
    num_words: usize,
    num_bytes: usize,
    num_chars: usize,
}

impl WcCounts {
    fn new() -> Self {
        WcCounts {
            num_lines: 0,
            num_words: 0,
            num_bytes: 0,
            num_chars: 0
        }
    }
}

fn compute_statistics(wc_args: WcOptions, mut reader: Box<dyn BufRead>) -> WcCounts {
    let mut total_counts = WcCounts::new();
    // let mut buffer: Vec<> = Vec::with_capacity(CHUNK_SIZE);
    let mut line_buffer = String::new();

    while let Ok(bytes_read) = reader.read_line(&mut line_buffer) {
        if bytes_read == 0 {
            break;
        }
        // Count bytes
        if wc_args.count_bytes {
            total_counts.num_bytes += bytes_read;
        }

        // Count lines
        if wc_args.count_lines {
            total_counts.num_lines += 1;
        }

        // Count words
        if wc_args.count_words {
            total_counts.num_words += line_buffer.split_whitespace().count();
        }

        // Count chars (UTF-8 characters)
        if wc_args.count_chars {
            total_counts.num_chars += line_buffer.chars().count();
        }

        line_buffer.clear();
    }
    total_counts
}

fn main() {
    let args: Vec<_> = env::args().collect();
    let mut file_path = None;

    // Solve args first
    // Variables for types of args
    // Check if arg length is atleast one
    if args.is_empty() {
        println!("wc command requires atleast 1 args");
        return;
    }

    let mut wc_args = WcOptions::new();

    for arg in args.iter().skip(1) {
        // Parse args
        match arg.as_str() {
            "-l" => wc_args.count_lines = true,
            "-w" => wc_args.count_words = true,
            "-c" => wc_args.count_bytes = true,
            "-m" => wc_args.count_chars = true,
            _ => {
                if arg.starts_with("-") {
                    eprintln!("Unknown flag: {}", arg);
                    return
                }
                else {
                    file_path = Some(arg)
                }
            }
        }
    }


    // If no flags specified, show all
    if !wc_args.count_lines && !wc_args.count_bytes && !wc_args.count_chars && !wc_args.count_words {
        wc_args.count_lines = true;
        wc_args.count_words = true;
        wc_args.count_bytes = true;
        wc_args.count_chars = true;
    }

    let reader: Box<dyn BufRead> = match file_path {
        None => Box::new(BufReader::new(io::stdin())),
        Some(filename) => Box::new(BufReader::new(fs::File::open(filename).unwrap()))
    };

    let total_counts = compute_statistics(wc_args, reader);
    println!("Total counts: {:?}", total_counts);
}



#[cfg(test)]
mod tests {
    use super::*;
    use std::fs::File;
    use std::io::Write;
    use std::io::Result;
    use tempfile::TempDir;

    fn create_temp_file(content: &str) -> Result<(String, TempDir)> {
        let dir = TempDir::new()?;
        let file_path = dir.path().join("temp.txt");
        let file_path_str = file_path.to_str().unwrap().to_string();

        let mut file = File::create(&file_path)?;
        file.write_all(content.as_bytes())?;

        Ok((file_path_str, dir))
    }

    #[test]
    fn test_count_empty_file() {
        let (file_path, _temp_dir) = create_temp_file("").unwrap();
        let file = File::open(&file_path).unwrap();
        let reader: Box<dyn BufRead> = Box::new(BufReader::new(file));

        let wc_args = WcOptions::new();
        let result = compute_statistics(wc_args, reader);
        assert_eq!(result, WcCounts::new());
    }


    #[test]
    fn test_count_test_wc_file() {
        let content = include_str!("../../../assets/test_wc.txt");
        let (file_path, _temp_dir) = create_temp_file(content).unwrap();
        let file = File::open(&file_path).unwrap();
        let reader: Box<dyn BufRead> = Box::new(BufReader::new(file));

        let wc_args = WcOptions {
            count_lines: true,
            count_words: true,
            count_bytes: true,
            count_chars: true,
        };
        let result = compute_statistics(wc_args, reader);
        assert_eq!(result, WcCounts {
            num_lines: 7145,
            num_words: 58164,
            num_bytes: 342190,
            num_chars: 339292,
        });
    }

    #[test]
    fn test_count_lines_only() {
        let content = "hello world\nline two\nline three";
        let (file_path, _temp_dir) = create_temp_file(content).unwrap();
        let file = File::open(&file_path).unwrap();
        let reader: Box<dyn BufRead> = Box::new(BufReader::new(file));

        let wc_args = WcOptions {
            count_lines: true,
            count_words: false,
            count_bytes: false,
            count_chars: false,
        };
        let result = compute_statistics(wc_args, reader);
        assert_eq!(result, WcCounts {
            num_lines: 3,
            num_words: 0,
            num_bytes: 0,
            num_chars: 0,
        });
    }

    #[test]
    fn test_count_words_only() {
        let content = "hello world\nline two\nline three";
        let (file_path, _temp_dir) = create_temp_file(content).unwrap();
        let file = File::open(&file_path).unwrap();
        let reader: Box<dyn BufRead> = Box::new(BufReader::new(file));

        let wc_args = WcOptions {
            count_lines: false,
            count_words: true,
            count_bytes: false,
            count_chars: false,
        };
        let result = compute_statistics(wc_args, reader);
        assert_eq!(result, WcCounts {
            num_lines: 0,
            num_words: 6,
            num_bytes: 0,
            num_chars: 0,
        });
    }

    #[test]
    fn test_count_bytes_only() {
        let content = "hello world\nline two\nline three";
        let (file_path, _temp_dir) = create_temp_file(content).unwrap();
        let file = File::open(&file_path).unwrap();
        let reader: Box<dyn BufRead> = Box::new(BufReader::new(file));

        let wc_args = WcOptions {
            count_lines: false,
            count_words: false,
            count_bytes: true,
            count_chars: false,
        };
        let result = compute_statistics(wc_args, reader);
        assert_eq!(result, WcCounts {
            num_lines: 0,
            num_words: 0,
            num_bytes: 31,
            num_chars: 0,
        });
    }

    #[test]
    fn test_count_chars_only() {
        let content = "hello world\nline two\nline three";
        let (file_path, _temp_dir) = create_temp_file(content).unwrap();
        let file = File::open(&file_path).unwrap();
        let reader: Box<dyn BufRead> = Box::new(BufReader::new(file));

        let wc_args = WcOptions {
            count_lines: false,
            count_words: false,
            count_bytes: false,
            count_chars: true,
        };
        let result = compute_statistics(wc_args, reader);
        assert_eq!(result, WcCounts {
            num_lines: 0,
            num_words: 0,
            num_bytes: 0,
            num_chars: 31,
        });
    }
}
