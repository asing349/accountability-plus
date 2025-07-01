import React, { useState, useEffect } from 'react';
import { Box, Flex, Input, Button, Text, VStack, Spinner, Heading, Container, Link, SimpleGrid, useMediaQuery } from '@chakra-ui/react';
import { motion } from 'framer-motion';
import TerminalWindow from './components/TerminalWindow';
import Footer from './components/Footer';

// Helper to parse entity strings
const parseEntityString = (entityString) => {
  if (!entityString) return [];
  const cleanedString = entityString
    .replace(/^(Accused|Victims|Organisations\/Courts|Outcome|Crime):\s*/, '')
    .replace(/;;\s*(Accused|Victims|Organisations\/Courts|Outcome|Crime):\s*/g, ';;');
  return cleanedString.split(/;;\s*|\s*,\s*/).map(item => item.trim()).filter(item => item !== '');
};

// --- Components --- //

// Header (minimalist, blends in)
const TerminalHeader = () => (
  <Box as="header" py={4} px={8} width="100%" textAlign="center">
    <Text fontSize={{ base: "2xl", md: "4xl" }} fontWeight="bold" color="accentBlue">
      ACCOUNTABILITY++
    </Text>
  </Box>
);

// CLI Input for Initial State
const CliInput = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  return (
    <TerminalWindow>
      <Flex as="form" onSubmit={handleSubmit} align="center" justify="center" width="100%">
        <Text color="terminalGreen" fontSize={{ base: "md", md: "lg" }} mr={2}>
          user@accountability-plus:~$
        </Text>
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query..."
          variant="unstyled"
          color="lightText" // Light grey for user input
          _placeholder={{ color: 'gray.500' }}
          fontSize={{ base: "md", md: "lg" }}
          fontFamily="monospace"
          isDisabled={isLoading}
          autoFocus
          width="100%"
        />
        <Button type="submit" display="none">Submit</Button> {/* Hidden submit for Enter key */}
      </Flex>
    </TerminalWindow>
  );
};

// Loading Screen (Data Stream)
const LoadingScreen = () => {
  const messages = [
    "[STATUS] Initializing secure protocols...",
    "[TASK] Querying external data sources...",
    "[PROGRESS] Analyzing data streams...",
    "[TASK] Synthesizing comprehensive narrative...",
    "[STATUS] Extracting entities...",
    "[COMPLETE] Finalizing report...",
  ];
  const [currentMessage, setCurrentMessage] = useState(messages[0]);
  const [logLines, setLogLines] = useState([]);

  useEffect(() => {
    let messageIndex = 0;
    const interval = setInterval(() => {
      const newMessage = messages[messageIndex];
      setLogLines((prev) => [...prev, newMessage]);
      setCurrentMessage(newMessage);
      messageIndex = (messageIndex + 1) % messages.length;
    }, 2000); // Change message every 2 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <Flex
      direction="column"
      align="center"
      justify="center"
      height="100vh"
      width="100vw"
      bg="rgba(0,0,0,0.95)"
      position="fixed"
      top="0"
      left="0"
      zIndex={9999}
      color="terminalGreen"
      fontFamily="monospace"
      overflow="hidden"
    >
      <VStack spacing={2} mb={8} maxH="70vh" overflowY="auto" px={4} width="100%">
        {logLines.map((line, index) => (
          <Text key={index} fontSize={{ base: "sm", md: "md" }} opacity={1 - (logLines.length - 1 - index) * 0.1}>
            {line}
          </Text>
        ))}
      </VStack>
      <Spinner size="xl" color="terminalGreen" mb={4} />
      <Text fontSize={{ base: "lg", md: "xl" }} textAlign="center">
        {currentMessage}
      </Text>
    </Flex>
  );
};

// Dashboard for Results
const Dashboard = ({ data, onNewQuery }) => {
  const { query, summary_text, entity_output, websearch_output } = data;

  const cleanSummaryText = (text) => {
    if (!text) return '';
    return text.replace(/\*\*/g, ''); // Remove Markdown bold syntax
  };

  const parsedEntities = {
    accused: entity_output?.accused ? parseEntityString(entity_output.accused.join(', ')) : [],
    victims: entity_output?.victims ? parseEntityString(entity_output.victims.join(', ')) : [],
    orgs: entity_output?.orgs ? parseEntityString(entity_output.orgs.join(', ')) : [],
    crime: entity_output?.crime || '',
    verdict: entity_output?.verdict || '',
    outcome: entity_output?.outcome || '',
  };

  const [isLargerThanMd] = useMediaQuery("(min-width: 48em)");

  return (
    <Container maxW="container.xl" py={8} fontFamily="monospace">
      <VStack spacing={8} align="stretch">
        {/* Query Panel */}
        <Box p={6} borderWidth="1px" borderColor="gray.700" borderRadius="md" bg="gray.900">
          <Heading size="md" color="terminalBlue" mb={4}>&gt; Query:</Heading>
          <Text fontSize="lg" color="whiteAlpha.900" textAlign="left">{query}</Text>
        </Box>

        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={8}>
          {/* Comprehensive Narrative */}
          <Box p={6} borderWidth="1px" borderColor="gray.700" borderRadius="md" bg="gray.900">
            <Heading size="md" color="terminalBlue" mb={4}>&gt; Comprehensive Narrative:</Heading>
            <Box maxH="500px" overflowY="auto">
              {summary_text ? (
                cleanSummaryText(summary_text).split('\n').map((paragraph, index) => (
                  <Text key={index} mb={2} textAlign="left">
                    {paragraph}
                  </Text>
                ))
              ) : (
                <Text>No summary available.</Text>
              )}
            </Box>
          </Box>

          {/* Key Entities */}
          <Box p={6} borderWidth="1px" borderColor="gray.700" borderRadius="md" bg="gray.900">
            <Heading size="md" color="terminalBlue" mb={4}>&gt; Key Entities:</Heading>
            <VStack align="stretch" spacing={2}>
              {parsedEntities.accused.length > 0 && (
                <Text><strong>Accused:</strong> {parsedEntities.accused.join(', ')}</Text>
              )}
              {parsedEntities.victims.length > 0 && (
                <Text><strong>Victims:</strong> {parsedEntities.victims.join(', ')}</Text>
              )}
              {parsedEntities.orgs.length > 0 && (
                <Text><strong>Organizations/Courts:</strong> {parsedEntities.orgs.join(', ')}</Text>
              )}
              {parsedEntities.crime && (
                <Text><strong>Crime:</strong> {parsedEntities.crime}</Text>
              )}
              {parsedEntities.verdict && (
                <Text><strong>Verdict:</strong> {parsedEntities.verdict}</Text>
              )}
              {parsedEntities.outcome && (
                <Text><strong>Outcome:</strong> {parsedEntities.outcome}</Text>
              )}
            </VStack>
            {(!parsedEntities.accused.length && !parsedEntities.victims.length && !parsedEntities.orgs.length && !parsedEntities.crime && !parsedEntities.verdict && !parsedEntities.outcome) && (
              <Text>No entities extracted.</Text>
            )}
          </Box>
        </SimpleGrid>

        {/* Reference Links */}
        <Box p={6} borderWidth="1px" borderColor="gray.700" borderRadius="md" bg="gray.900">
          <Heading size="md" color="terminalBlue" mb={4}>&gt; Reference Links:</Heading>
          {websearch_output && (websearch_output.most_relevant || websearch_output.most_recent) ? (
            <VStack align="flex-start" spacing={1}>
              {[...(websearch_output.most_relevant || []), ...(websearch_output.most_recent || [])]
                .filter((link, index, self) => 
                  index === self.findIndex((t) => t.url === link.url)
                ) // Deduplicate links
                .map((link, index) => (
                  <Link key={index} href={link.url} isExternal color="terminalBlue" _hover={{ textDecoration: 'underline' }}>
                    {link.title || link.url}
                    {link.source && link.source.name && (
                      <Text as="span" fontSize="sm" color="gray.500"> ({link.source.name})</Text>
                    )}
                  </Link>
                ))}
            </VStack>
          ) : (
            <Text>No reference links found.</Text>
          )}
        </Box>
        <Flex justify="center" mt={8}>
          <Button onClick={onNewQuery} colorScheme="blue" variant="outline">
            New Query
          </Button>
        </Flex>
      </VStack>
    </Container>
  );
};

// --- Main App Component --- //
function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSearch = async (query) => {
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleNewQuery = () => {
    setResult(null);
    setError(null);
  };

  return (
    <Flex direction="column" minH="100vh" bg="darkBackground" color="lightText" fontFamily="monospace">
      <TerminalHeader />
      <Flex flex={1} align="center" justify="center" p={4}>
        {!loading && !result && !error && (
          <CliInput onSearch={handleSearch} isLoading={loading} />
        )}

        {loading && <LoadingScreen />}

        {error && (
          <VStack spacing={4} p={8} bg="red.900" borderRadius="md" boxShadow="lg" maxW="md" textAlign="center">
            <Text fontSize="xl" color="red.300">Error Occurred</Text>
            <Text color="red.100">{error}</Text>
            <Button onClick={() => setError(null)} colorScheme="red" variant="outline">
              Try Again
            </Button>
          </VStack>
        )}

        {result && !loading && !error && (
          <Dashboard data={result} onNewQuery={handleNewQuery} />
        )}
      </Flex>
      <Footer />
    </Flex>
  );
}

export default App;