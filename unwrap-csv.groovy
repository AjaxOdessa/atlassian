/*
	Created by Yevgen Lasman on Oct-26 '16

	Script converts file input.csv file with structure
		record1, value1
		record1, value2
		record2, value1
		record3, value1
		record3, value6
	into Groovy HashMap
		record1:value1,value2
		record2:value1
		record3:value1,value6
	Can be used to convert into importable CSV for JIRA issues update/import.
*/

@Grab('org.apache.commons:commons-csv:1.2')
import org.apache.commons.csv.CSVParser
import static org.apache.commons.csv.CSVFormat.*

import java.nio.file.Paths

def map = new HashMap()

Paths.get("input.csv").withReader {
	CSVParser csv = new CSVParser(it, DEFAULT.withHeader())

	for (record in csv.iterator()) {
		def key = record[0]
		def value = record[1]
		if (value != "#N/A") {
			if (map.get(key)) {
				def tval = map.get(key)
				def wval = "${tval.toString()},${value.toString()}"
				map.put(key, wval)
			} else {
				map.put(key, value)
			}
		}
	}
}
