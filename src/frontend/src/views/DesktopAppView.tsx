import { useEffect } from 'react';
import { RouterProvider } from '@tanstack/react-router';

import { getBaseUrl } from '@lib/functions/Navigation';
import { useShallow } from 'zustand/react/shallow';
import { api, queryClient } from '../App';
import { ApiProvider } from '../contexts/ApiContext';
import { ThemeContext } from '../contexts/ThemeContext';
import { defaultHostList } from '../defaults/defaultHostList';
import { router } from '../router-tanstack';
import { useLocalState } from '../states/LocalState';

export default function DesktopAppView() {
  const [hostList] = useLocalState(useShallow((state) => [state.hostList]));

  useEffect(() => {
    if (Object.keys(hostList).length === 0) {
      useLocalState.setState({ hostList: defaultHostList });
    }
  }, [hostList]);

  // Update router basepath
  useEffect(() => {
    const basePath = getBaseUrl();
    if (basePath && router.basepath !== `/${basePath}`) {
      router.update({
        basepath: `/${basePath}`
      });
    }
  }, []);

  return (
    <ApiProvider client={queryClient} api={api}>
      <ThemeContext>
        <RouterProvider router={router} />
      </ThemeContext>
    </ApiProvider>
  );
}
