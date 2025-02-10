import { BackgroundImage, Center, Container } from '@mantine/core';
import { useEffect, useMemo } from 'react';
import { Outlet } from 'react-router-dom';
import { generateUrl } from '../../functions/urls';
import { useServerApiState } from '../../states/ApiState';

export default function LayoutComponent() {
  const [server, fetchServerApiState] = useServerApiState((state) => [
    state.server,
    state.fetchServerApiState
  ]);

  const SplashComponent = useMemo(() => {
    const temp = server.customize?.splash;
    if (temp) {
      return ({ children }: { children: React.ReactNode }) => (
        <BackgroundImage src={generateUrl(temp)}>{children}</BackgroundImage>
      );
    }
    return ({ children }: { children: React.ReactNode }) => <>{children}</>;
  }, [server.customize]);

  // Fetch server data on mount if no server data is present
  useEffect(() => {
    if (server.server === null) {
      fetchServerApiState();
    }
  }, [server]);

  // Main rendering block
  return (
    <SplashComponent>
      <Center mih='100vh'>
        <div
          style={{
            padding: '10px',
            backgroundColor: 'rgba(0,0,0,0.5)',
            boxShadow: '0 0 15px 10px rgba(0,0,0,0.5)'
          }}
        >
          <Container w='md' miw={400}>
            <Outlet />
          </Container>
        </div>
      </Center>
    </SplashComponent>
  );
}
