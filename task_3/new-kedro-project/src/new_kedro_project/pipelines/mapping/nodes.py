"""
This is a boilerplate pipeline 'mapping'
generated using Kedro 1.4.0
"""
import subprocess
import re

def run_fastqc(fastq_1: str, fastq_2: str):
    """Узел для запуска FastQC """
    print(f"[*] Запуск FastQC для {fastq_1} и {fastq_2}...")
    subprocess.run(["fastqc", fastq_1, fastq_2], check=False)
    return "qc_report_done"

def run_mapping(ref_index: str, fastq_1: str, fastq_2: str, qc_status: str):
    """Узел для картирования и конвертации в BAM """
    print(f"[*] Статус QC: {qc_status}")
    print("[*] Выполнение картирования (minimap2) и конвертации (samtools view)...")
    output_bam = "data/02_intermediate/alignment.bam"
    cmd = f"minimap2 -a -x sr {ref_index} {fastq_1} {fastq_2} | samtools view -b -o {output_bam}"
    subprocess.run(cmd, shell=True, check=True)
    return output_bam

def run_flagstat(bam_file: str):
    """Узел для сбора статистики """
    print("[*] Сбор статистики (samtools flagstat)...")
    report_file = "data/02_intermediate/flagstat_report.txt"
    cmd = f"samtools flagstat {bam_file} > {report_file}"
    subprocess.run(cmd, shell=True, check=True)
    return report_file

def evaluate_mapping(report_file: str):
    """Узел парсинга и принятия решения """
    print("[*] Парсинг результатов и оценка качества...")
    mapped_percent = 0.0

    with open(report_file, 'r') as file:
        for line in file:
            if " mapped (" in line and "primary" not in line:
                match = re.search(r'\((\d+\.\d+)% :', line)
                if match:
                    mapped_percent = float(match.group(1))
                    break

    print(f"    -> Доля картированных ридов: {mapped_percent}%")

    if mapped_percent > 90.0:
        print("\n=> ОЦЕНКА: OK")
        return "OK"
    else:
        print("\n=> ОЦЕНКА: not OK")
        return "not OK"
