import legislation

def get_text_from_file(filename):
    with open(filename, 'r') as file:
        text = file.read()
    return text

def get_legislations():
    ccr_text = get_text_from_file("resource/ccr.txt")
    mmc_text = get_text_from_file("resource/mmc.txt")
    ntf_text = get_text_from_file("resource/ntf.txt")

    return [
        legislation.Legislation(
            title="Climate Change Resiliency Fund for America Act of 2023",
            description=ccr_text,
            summary="""
This bill provides support to address the impacts of climate change.
Specifically, the bill authorizes the Department of the Treasury to issue up to $1 billion in climate change obligations (e.g., bonds) in a fiscal year, with bond proceeds going into the Climate Change Resiliency Fund established by this bill. The fund must be used for a program that finances projects that reduce the economic, social, and environmental impact of the adverse effects of climate change. A percentage of those funds must be used to benefit communities that experience disproportionate impacts from climate change.
The Climate Change Advisory Commission, established by this bill, must provide recommendations and guidelines for the program and identify categories of the most cost-effective investments and projects that emphasize multiple benefits to commerce, human health, and ecosystems.
 """,
            region="USA",
            status="Introduced",
            type_="Environmental Protection",
            index="ccr",
            date="12/06/2023",
            link="https://www.congress.gov/bill/118th-congress/senate-bill/3416?q=%7B%22search%22:%22climate%22%7D&s=1&r=6"
        ),
        legislation.Legislation(
            title="Marine Mammal Climate Change Protection Act",
            description=mmc_text,
            summary="""
This bill establishes requirements to protect marine mammals adversely affected by climate change, including by establishing a program within the National Oceanic and Atmospheric Administration (NOAA) to monitor the adverse impacts of climate change on marine mammals.
In addition, it also requires NOAA's National Marine Fisheries Service (NMFS) and the U.S. Fish and Wildlife Service (USFWS) to issue regulations that list marine mammal species in waters under U.S. jurisdiction for which climate change is more likely than not to result in a decline in population abundance, an impeded population recovery, or a reduced carrying capacity (i.e., the maximum population of a marine mammal species that an area will support without undergoing deterioration). The NMFS and the USFWS must update the list at least once every five years and issue regulations that include climate impact management plans for species on such list.
The bill also directs the NMFS and the USFWS to review agreements with foreign governments concerning the management of marine mammals that are or may be affected by climate change. The Department of State must initiate amendments to such agreements or negotiate the development of such agreements in a manner consistent with the goals of the bill.
""",
            region="USA",
            status="Introduced",
            type_="Environmental Protection",
            index="mmc",
            date="03/07/2023",
            link="https://www.congress.gov/bill/118th-congress/house-bill/1383?s=1&r=14&q=%7B%22search%22:%22climate%22%7D"
        ),
        legislation.Legislation(
            title="",
            description="",
            summary="",
            region="",
            status="",
            type_="",
            index="",
            date="",
            link=""
        )
    ]
