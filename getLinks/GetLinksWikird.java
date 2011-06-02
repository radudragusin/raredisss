import java.io.IOException;

public class GetLinksWikird {
	public static void main(String[] args) throws IOException {
		
		String resourceName = "wikird";
		String link = "http://en.wikipedia.org/w/api.php?action=query&" +
				"generator=categorymembers&gcmtitle=Category:Rare_diseases&" +
				"gcmlimit=max&gcmdir=asc&export&exportnowrap\n";
		
		new GetBulkLinks(resourceName,link);

	}
}
