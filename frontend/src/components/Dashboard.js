import React from 'react';
import { Box, Flex, Text, VStack, Heading, Container, Link, SimpleGrid, Tag, TagLabel } from '@chakra-ui/react';

// Helper to parse entity strings
const parseEntityString = (entityString) => {
  if (!entityString) return [];
  const cleanedString = entityString
    .replace(/^(Accused|Victims|Organisations\/Courts|Outcome|Crime):\s*/, '')
    .replace(/;;\s*(Accused|Victims|Organisations\/Courts|Outcome|Crime):\s*/g, ';;');
  return cleanedString.split(/;;\s*|\s*,\s*/).map(item => item.trim()).filter(item => item !== '');
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
            <Heading size="lg" color="terminalBlue" mb={4}>&gt; Key Entities:</Heading> {/* Increased heading size */}
            <VStack align="stretch" spacing={2}>
              {parsedEntities.accused.length > 0 && (
                <Flex wrap="wrap" mb={2}>
                  <Text as="strong" mr={2}>Accused:</Text>
                  {parsedEntities.accused.map((person, idx) => (
                    <Tag size="md" key={idx} variant="subtle" colorScheme="red" mr={1} mb={1}>
                      <TagLabel>{person}</TagLabel>
                    </Tag>
                  ))}
                </Flex>
              )}
              {parsedEntities.victims.length > 0 && (
                <Flex wrap="wrap" mb={2}>
                  <Text as="strong" mr={2}>Victims:</Text>
                  {parsedEntities.victims.map((person, idx) => (
                    <Tag size="md" key={idx} variant="subtle" colorScheme="orange" mr={1} mb={1}>
                      <TagLabel>{person}</TagLabel>
                    </Tag>
                  ))}
                </Flex>
              )}
              {parsedEntities.orgs.length > 0 && (
                <Flex wrap="wrap" mb={2}>
                  <Text as="strong" mr={2}>Organizations/Courts:</Text>
                  {parsedEntities.orgs.map((org, idx) => (
                    <Tag size="md" key={idx} variant="subtle" colorScheme="purple" mr={1} mb={1}>
                      <TagLabel>{org}</TagLabel>
                    </Tag>
                  ))}
                </Flex>
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

export default Dashboard;
