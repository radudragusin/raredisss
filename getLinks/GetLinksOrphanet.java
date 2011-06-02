import java.io.IOException;

public class GetLinksOrphanet {
	public static void main(String[] args) throws IOException {
		
		String resourceName = "orphanet";
		String ftpLinks = "http://dragusin.ro/orpha.zip\n";
		
		new GetBulkLinks(resourceName,ftpLinks);

	}
}
